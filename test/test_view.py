from visset.view import View
from unittest import mock, TestCase


class TestView(TestCase):

    def setUp(self) -> None:
        self.keyboard = mock.patch('visset.view.InlineKeyboardMarkup', spec = True).start()
        self.button = mock.patch('visset.view.InlineKeyboardButton', spec = True).start()
        self.language = mock.patch('visset.languages.Language.get_all').start()

        self.clip = mock.patch('visset.models.Clip', spec = True).start()
        self.clip.return_value.to_inline.return_value = ...

        self.language.return_value = [
            self.language('english', 'English US', {}),
            self.language('portuguese', 'Português BR', {})
        ]

    def test_get_language_keyboard_markup(self) -> None:
        expected = self.keyboard()

        expected.add(self.button('english', 'English US'))
        expected.add(self.button('portuguese', 'Português BR'))

        self.assertEqual(expected, View.get_language_reply_markup())

    def test_get_inline_answer(self) -> None:
        self.assertListEqual([..., ..., ...], View.get_clips_inline_answer(self.clip() for i in range(3)))

    def tearDown(self) -> None:
        self.language.stop()
