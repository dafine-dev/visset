from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .session import Session
    from .exception_handler import ExceptionHandler


class AcervoException(Exception):

    def accept(self, handler: type[ExceptionHandler]) -> bool:
        return handler.on_any(self)


class OnSessionException(AcervoException):
    on_session: Session

    def __init__(self, *args: object, on_session: Session = ...) -> None:
        super().__init__(*args)
        self.on_session = on_session


class UnexpectedActionException(OnSessionException):
    notification: bool = False

    def __init__(self, *args: object, on_session: Session = ..., notification: bool = False, callback_id: int = ...) -> None:
        super().__init__(*args, on_session = on_session)
        self.notification = notification
        self.callback_id = callback_id

    def accept(self, handler: type[ExceptionHandler]) -> bool:
        return handler.on_unexpected_action(self)


class UnsupportedLanguageException(OnSessionException):
    language: str

    def __init__(self, *args: object, on_session: Session = ..., language: str = ...) -> None:
        super().__init__(*args, on_session = on_session)
        self.language = language

    def accept(self, handler: type[ExceptionHandler]) -> bool:
        return handler.on_unsupported_language(self)


class UnsupportedMediaType(OnSessionException):
    media_type: str

    def __init__(self, *args: object, on_session: Session = ..., media_type: str = ...) -> None:
        super().__init__(*args, on_session = on_session)
        self.media_type = media_type

    def accept(self, handler: type[ExceptionHandler]) -> bool:
        return handler.on_supported_media_type(self)


class DatabaseTransactionException(AcervoException):
    ...


class UploadClipException(OnSessionException):

    def accept(self, handler: type[ExceptionHandler]) -> bool:
        return handler.on_upload_clip(self)


class IncompleteClipSavingAttemptException(AcervoException):
    ...
