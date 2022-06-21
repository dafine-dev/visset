from unittest import TestCase, mock
from visset.errors import DatabaseTransactionException
from visset.errors import UploadClipException
from visset.models import Clip


class TestController(TestCase):

    def setUp(self) -> None:
        self.bot = mock.patch('visset.controllers.bot').start()
        self.service = mock.patch('visset.controllers.ClipService', spec = True).start()
        self.session = mock.patch('visset.controllers.Session', spec = True).start()
        self.message = mock.patch('telebot.types.Message', spec = True).start()
        self.callback = mock.patch('telebot.types.CallbackQuery', spec = True).start()
        self.inline_query = mock.patch('telebot.types.InlineQuery', spec = True).start()
        self.view = mock.patch('visset.controllers.View', spec = True).start()

        from visset.controllers import Controller
        self.controller = Controller()

    def test_handle_message(self) -> None:
        self.controller.handle_message(self.message())

    def test_handle_media(self) -> None:
        self.controller.handle_media(self.message())

    def test_handle_callback(self) -> None:
        self.controller.handle_callback(self.callback())

    def test_handle_set_language(self) -> None:
        self.controller.handle_set_language(self.message())

    def test_handle_start(self) -> None:
        self.controller.handle_start(self.message())

    def test_handle_inline_query_with_no_more_results(self) -> None:
        self.inline_query.return_value.id = 1
        self.inline_query.return_value.offset = 1
        self.view.get_clips_inline_answer.return_value = ...

        self.controller._clip_service.get_by_description.return_value = []
        self.controller.handle_inline_query(self.inline_query())
        self.bot.answer_inline_query.assert_any_call(1, ..., '')

    def test_handle_inline_query_with_more_results(self) -> None:
        self.inline_query.return_value.id = 1
        self.inline_query.return_value.offset = 1

        self.view.get_clips_inline_answer.return_value = ...

        self.controller._clip_service.get_by_description.return_value = [...]
        self.controller.handle_inline_query(self.inline_query())
        self.bot.answer_inline_query.assert_any_call(1, ..., '2')

    def test_save_clip(self) -> None:
        self.controller._clip_service.save_clip
        self.controller.save_clip(self.session(), Clip())

    def test_save_clip_with_error(self) -> None:
        self.controller._clip_service.save_clip.side_effect = DatabaseTransactionException
        with self.assertRaises(UploadClipException):
            self.controller.save_clip(self.session(), Clip())

    def test_send_language_keyboard(self) -> None:
        self.controller.send_language_keyboard(self.session(), 'prompt example')

    def test_send_message(self) -> None:
        self.controller.send_message(self.session(), 'prompt example')

    def test_notify(self) -> None:
        self.controller.notify(1, 'prompt example')

    def test_edit_message(self) -> None:
        self.session.return_value.id = 1
        self.controller.edit_message(self.session(), 1, 'prompt example')
