from __future__ import annotations
from typing import TYPE_CHECKING
from telebot import types

from .utils import abstract

if TYPE_CHECKING:
    from .session import Session


@abstract
class Context:

    def on_message(self, session: Session, msg: types.Message) -> None:
        raise UnexpectedActionException(on_session = session, notification = False)

    def on_media(self, session: Session, msg: types.Message) -> None:
        raise UnexpectedActionException(on_session = session, notification = False)

    def on_callback(self, session: Session, callback: types.CallbackQuery) -> None:
        raise UnexpectedActionException(on_session = session, notification = True, callback_id = callback.id)


class SetLanguageContext(Context):

    def on_callback(self, session: Session, callback: types.CallbackQuery) -> None:
        session._update_language(callback)
        session._context = PostClipContext()

    def on_media(self, session: Session, msg: types.Message) -> None:
        session._context = PostClipContext()
        session._update_clip_media(msg)

    def on_message(self, session: Session, msg: types.Message) -> None:
        session._context = PostClipContext()
        session._update_description(msg)


class PostClipContext(Context):

    def on_message(self, session: Session, msg: types.Message) -> None:
        session._update_description(msg)

    def on_media(self, session: Session, msg: types.Message) -> None:
        session._update_clip_media(msg)


class ReportContext(Context):
    ...


from .errors import UnexpectedActionException
