from __future__ import annotations
from telebot.types import Message, CallbackQuery
from .context import Context, PostClipContext, SetLanguageContext
from .utils import self_factory


@self_factory
class Session:
    id: int | str
    _clip: Clip
    _context: Context = PostClipContext()
    _language: Language

    def __init__(self, id: int | str) -> None:
        self.id = id
        self._clip = Clip()
        self._language = Language.get('english')

    @property
    def language(self) -> Language:
        return self._language

    @language.setter
    def language(self, name: str) -> None:
        if Language.validate(name):
            self._language = Language.get(name)
        else:
            raise UnsupportedLanguageException(on_session = self, language = name)

    def _update_language(self, callback: CallbackQuery) -> None:
        self.language = callback.data
        Controller().edit_message(self, callback.message.id, self._language.get_prompt('language_set'))

    def _update_clip_media(self, msg: Message) -> None:
        controller = Controller()
        if self._clip.telegram_file_id is not None:
            controller.send_message(self, self._language.get_prompt('media_updated'))

        try:
            self._clip.type = MediaTypes[msg.content_type]
        except KeyError:
            raise UnsupportedMediaType(on_session = self, media_type = msg.content_type)

        self._clip.from_message(msg)

        if self._clip.description is None:
            controller.send_message(self, self._language.get_prompt('send_description'))
        else:
            controller.save_clip(self, self._clip)
            self._clip = Clip()

    def _update_description(self, msg: Message) -> None:
        controller = Controller()
        if self._clip.description is not None:
            controller.send_message(self, self._language.get_prompt('description_updated'))

        self._clip.description = msg.text

        if self._clip.telegram_file_id is None:
            controller.send_message(self, self._language.get_prompt('send_media'))
        else:
            controller.save_clip(self, self._clip)
            self._clip = Clip()

    def _set_report_text(self, msg: Message) -> None:
        raise NotImplementedError

    def handle_start_command(self, msg: Message) -> None:
        Controller().send_message(self, self._language.get_prompt('start'))

    def handle_set_language_command(self, msg: Message) -> None:
        Controller().send_language_keyboard(self, self._language.get_prompt('choose_language'))
        self._context = SetLanguageContext()

    def handle_cancel_command(self, msg: Message) -> None:
        Controller().send_message(self, self._language.get_prompt('cancel'))
        self._clip = Clip()
        self._context = PostClipContext()

    def handle_message(self, msg: Message) -> None:
        self._context.on_message(self, msg)

    def handle_callback(self, callback: CallbackQuery) -> None:
        self._context.on_callback(self, callback)

    def handle_media(self, msg: Message) -> None:
        self._context.on_media(self, msg)


from .errors import UnsupportedLanguageException, UnsupportedMediaType
from .models import Clip, MediaTypes
from .languages import Language
from .controllers import Controller
