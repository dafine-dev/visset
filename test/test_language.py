from unittest import TestCase, mock
from visset.languages import Language


class TestLanguage(TestCase):

    def setUp(self) -> None:
        languages = [{'inner_name': 'english', 'view_name': 'English', 'prompts': {'example': 'prompt example !'}}]
        self.open = mock.patch('builtins.open').start()
        self.load = mock.patch('json.load', return_value = languages).start()
        Language.start()

    def assert_language(self, language, base_language):
        assert language.inner_name == base_language.inner_name
        assert language.view_name == base_language.view_name
        assert language._prompts == base_language._prompts

    def test_start(self) -> None:
        Language.start()

    def test_create(self) -> None:
        language = Language.create('portuguese', 'Português', {'example': 'prompt exemplo !'})
        self.assertEqual(Language._instances['portuguese'], language)

    def test_get_all(self) -> None:
        languages = [language for language in Language.get_all()]
        self.assert_language(languages[0], Language('english', 'English', {'example': 'prompt example !'}))
        self.assert_language(languages[1], Language('portuguese', 'Português', {'example': 'prompt exemplo !'}))

    def test_get(self) -> None:
        self.assert_language(Language.get('english'), Language('english', 'English', {'example': 'prompt example !'}))

    def test_get_with_error(self) -> None:
        with self.assertRaises(KeyError):
            Language.get('spanish')

    def test_validate_valid_language(self) -> None:
        self.assertTrue(Language.validate('english'))

    def test_validate_invalid_language(self) -> None:
        self.assertFalse(Language.validate('spanish'))

    def test_get_prompt(self) -> None:
        self.assertEqual(Language.get('english').get_prompt('example'), 'prompt example !')

    def test_get_prompt_with_error(self) -> None:
        with self.assertRaises(KeyError):
            Language.get('english').get_prompt('inexistent_prompt')
