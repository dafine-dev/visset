from unittest import TestCase, mock
from visset.context import PostClipContext, SetLanguageContext
from visset.errors import UnexpectedActionException


class TestPostClipContext(TestCase):

    def setUp(self) -> None:
        self.context = PostClipContext()
        self.session = mock.patch('visset.session.Session', spec = True).start()
        self.session.id = 1
        self.message = mock.patch('telebot.types.Message', spec = True).start()
        self.callback = mock.patch('telebot.types.CallbackQuery', spec = True).start()
        self.callback.id = 1

    def test_on_message(self) -> None:
        self.context.on_message(self.session, self.message)
        self.session._update_description.assert_called()

    def test_on_callback(self) -> None:
        with self.assertRaises(UnexpectedActionException):
            self.context.on_callback(self.session, self.callback)

    def test_on_media(self) -> None:
        self.context.on_media(self.session, self.message)
        self.session._update_clip_media.assert_called()


class TestSetLanguageContext(TestCase):

    def setUp(self) -> None:
        self.context = SetLanguageContext()
        self.session = mock.patch('visset.session.Session', spec = True).start()
        self.message = mock.patch('telebot.types.Message', spec = True).start()
        self.callback = mock.patch('telebot.types.CallbackQuery', spec = True).start()

    def test_on_message(self) -> None:
        self.context.on_message(self.session, self.message)

    def test_on_callback(self) -> None:
        self.context.on_callback(self.session, self.callback)

    def test_on_media(self) -> None:
        self.context.on_media(self.session, self.message)
