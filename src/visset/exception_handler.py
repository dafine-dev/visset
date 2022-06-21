from __future__ import annotations
from .utils import abstract


@abstract
class ExceptionHandler:

    @staticmethod
    def on_any(exception: Exception) -> bool:
        return False

    @staticmethod
    def on_upload_clip(exception: UploadClipException) -> bool:
        Controller().send_message(exception.on_session, prompt = exception.on_session.language.get_all('upload_error'))

        return True

    @staticmethod
    def on_unexpected_action(exception: UnexpectedActionException) -> bool:
        controller = Controller()
        if exception.notification:
            controller.notify(callback_id = exception.callback_id, prompt = exception.on_session.language.get_prompt('unexpected_action'))
        else:
            controller.send_message(exception.on_session, prompt = exception.on_session.language.get_prompt('unexpected_action'))

        return True

    @staticmethod
    def on_unsupported_language(exception: UnsupportedLanguageException) -> bool:
        Controller().notify(exception.on_session, callback_query_id = exception.id, prompt = exception.on_session.language.get_prompt('invalid_language'))
        return True

    @staticmethod
    def on_supported_media_type(exception: UnsupportedMediaType) -> bool:
        Controller().send_message(exception.on_session, prompt = exception.on_session.language.get_prompt('invalid_media_type'))
        return True


from .controllers import Controller
from .errors import UnsupportedMediaType, UploadClipException, UnexpectedActionException, UnsupportedLanguageException
