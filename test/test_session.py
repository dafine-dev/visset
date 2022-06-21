from unittest import TestCase, mock
from visset.session import Session
from visset.errors import UnsupportedLanguageException, UnsupportedMediaType


class TestSession(TestCase):

    def setUp(self) -> None:
        self.language = mock.patch('visset.session.Language').start()
        self.language.get.return_value = self.language
        self.language.get_prompt.return_value = 'prompt example'
        self.controller = mock.patch('visset.session.Controller', spec = True).start()
        self.callback = mock.patch('telebot.types.CallbackQuery', spec = True).start()
        self.context = mock.patch('visset.session.Context', spec = True).start()
        self.message = mock.patch('telebot.types.Message', spec = True).start()
        self.message.return_value.content_type = 'photo'
        self.message.return_value.photo.file_id = '54as86d7ds86fh7ad7f'

    def test_language_setter(self):
        self.language.validate.return_value = True
        session = Session(id = 1)
        session.language = 'english'

        self.assertEqual(session._language, self.language)

    def test_invalid_language_setter(self):
        self.language.validate.return_value = False
        with self.assertRaises(UnsupportedLanguageException):
            Session(id = 1).language = 'spanish'

    def test_update_language(self):
        Session(id = 1)._update_language(self.callback())

    def test_set_clip_media(self):
        session = Session(id = 2)
        session._clip.telegram_file_id = None
        session._clip.description = None

        session._update_clip_media(self.message())
        self.language.get_prompt.assert_any_call('send_description')

    def test_update_media(self):
        session = Session(id = 3)
        session._clip.telegram_file_id = 'asd78gqew8r7a58a7g'

        session._update_clip_media(self.message())

    def test_update_media_save_clip(self):
        session = Session(id = 4)
        session._clip.description = 'description example'

        session._update_clip_media(self.message())
        self.controller.return_value.save_clip.assert_called_once()

    def test_update_unsuported_clip_media(self):
        self.message.return_value.content_type = 'audio'
        self.message.return_value.audio.file_id = 'ad5s78gqaew8g7ta8g'

        session = Session(id = 3)
        session._clip.telegram_file_id = None
        session._clip.description = None
        with self.assertRaises(UnsupportedMediaType):
            session._update_clip_media(self.message())

    def test_set_clip_description(self):
        session = Session(id = 3)
        session._clip.telegram_file_id = None
        session._clip.description = None

        session._update_description(self.message())
        self.language.get_prompt.assert_any_call('send_media')

    def test_update_description(self):
        session = Session(id = 4)
        session._clip.description = 'description example'

        session._update_description(self.message())

    def test_description_media_save_clip(self):
        session = Session(id = 4)
        session._clip.telegram_file_id = 'asd78gqew8r7a58a7g'

        session._update_description(self.message())

        self.controller.return_value.save_clip.assert_called_once()

    def test_handle_start_command(self):
        Session(id = 5).handle_start_command(self.message())
        self.controller.return_value.send_message.assert_called()

    def test_handle_set_language_command(self):
        Session(id = 6).handle_set_language_command(self.message())
        self.controller.return_value.send_language_keyboard.assert_called()

    def test_cancel_command(self):
        Session(id = 6).handle_cancel_command(self.message())
        self.controller.return_value.send_message.assert_called()

    def test_handle_message(self):
        Session(id = 1).handle_message(self.message())

    def test_handle_callaback(self):
        Session(id = 1).handle_message(self.callback())

    def test_handle_media(self):
        Session(id = 1).handle_media(self.message())
