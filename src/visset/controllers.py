from __future__ import annotations
from __main__ import bot
from telebot.types import Message, CallbackQuery, InlineQuery
from .utils import singleton


@singleton
class Controller:
    _clip_service: ClipService
    exception_handler: type[ExceptionHandler]

    def __init__(self) -> None:
        self._clip_service = ClipService()
        self.exception_handler = ExceptionHandler

    def __enter__(self) -> Controller:
        return self

    def __exit__(self, type: type[Exception], value: Exception, traceback) -> None:
        if isinstance(value, AcervoException):
            return value.accept(self.exception_handler)

        return False

    def save_clip(self, session: Session, clip: Clip) -> None:
        try:
            self._clip_service.save_clip(clip)
            bot.send_message(chat_id = session.id, text = session.language.get_prompt('clip_saved'))
        except DatabaseTransactionException:
            raise UploadClipException(on_session = session)

    def send_language_keyboard(self, session: Session, prompt: str) -> None:
        bot.send_message(chat_id = session.id, text = prompt, reply_markup = View.get_language_reply_markup())

    def send_message(self, session: Session, prompt: str) -> None:
        bot.send_message(chat_id = session.id, text = prompt)

    def notify(self, callback_id: int, prompt: str) -> None:
        bot.answer_callback_query(callback_id, text = prompt)

    def edit_message(self, session: Session, msg_id: int, prompt: str) -> None:
        bot.edit_message_text(chat_id = session.id, message_id = str(msg_id), text = prompt)

    def handle_start(self, msg: Message) -> None:
        Session(id = msg.chat.id).handle_start_command(msg)

    def handle_set_language(self, msg: Message) -> None:
        Session(id = msg.chat.id).handle_set_language_command(msg)

    def handle_cancel(self, msg: Message) -> None:
        Session(id = msg.chat.id).handle_cancel_command(msg)

    def handle_callback(self, callback: CallbackQuery) -> None:
        Session(id = callback.message.chat.id).handle_callback(callback)

    def handle_media(self, msg: Message) -> None:
        Session(id = msg.chat.id).handle_media(msg)

    def handle_message(self, msg: Message) -> None:
        Session(id = msg.chat.id).handle_message(msg)

    def handle_inline_query(self, inline_query: InlineQuery) -> None:
        wave = 1 if inline_query.offset in (None, '', ...) else int(inline_query.offset)
        clips = self._clip_service.get_by_description(inline_query.query, wave = wave)

        bot.answer_inline_query(
            inline_query.id,
            View.get_clips_inline_answer(clips),
            str(wave + 1) if len(clips) != 0 else ''
        )


from .errors import AcervoException, UploadClipException, DatabaseTransactionException
from .exception_handler import ExceptionHandler
from .service import ClipService
from .session import Session
from .models import Clip
from .view import View
