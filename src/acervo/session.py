from __future__ import annotations
from time import sleep
from typing import Any
from .utils import self_factory


class Session:
    _id: int | str
    _bot: TeleBot

    def __init__(self, id: int | str) -> None:
        self._id = id

    def __enter__(self) -> Session:
        ...

    def __exit__(self, type: type[Exception], value: Exception, traceback) -> bool:
        ...

    @classmethod
    def start_bot(cls, bot: TeleBot) -> None:
        if not isinstance(bot, TeleBot):
            raise TeleclipsException()
        
        cls._bot = bot

 

@self_factory
class UserSession(Session):
    _wave: int = 1
    _clip_service: ClipService = ClipService()

    async def _resolve_clips(self, description: str) -> None:
        results = self._clip_service.get_by_description(description, wave = self._wave)
        self._bot.answer_inline_query()
        ...
    
    def handle_inline_query(self, query: str, query_id: int | str) -> None:

        self._clip_service.get_by_description(description = query, wave = self._wave)
        



@self_factory
class ChatSession(Session):
    _clip: Clip
    _bot: TeleBot
    _chat_id: int
    _context: str = 'post_clip'
    _language: str = 'english'
    _clip_service: ClipService = ClipService()
        
    def __init__(self, id: int | str) -> None:
        super().__init__(id = id)
        self._clip = Clip()
    
    def __enter__(self) -> ChatSession:
        return self
    
    def __exit__(self, type: type[Exception], value: Exception, traceback) -> bool:
        match value:
            case UnsupportedLanguageException():
                self._send_message('invalid_language')
                return True
            case IncompleteClipSavingAttemptException():
                self._send_message('incomplete_clip_error')
                return True
            case _:
                return False
    
    @property
    def language(self) -> str:
        return self._language
    
    @language.setter
    def language(self, language: str) -> None:
        if Language.validate(language):
            self._language = language
        else:
            raise UnsupportedLanguageException(language = language)

    def _handle_clip_description(self, text: str) -> None:
        if self._clip.description is None:
            self._send_message('description_updated')
        
        self._clip.description = text

        sleep(2)

        if self._clip.telegram_file_id is None:
            self._send_message('send_media')
        else:
            self._save_clip()
    
    def _handle_set_language(self, data: Any, msg_id: str | int) -> None:
        self.language = data
        self._bot.edit_message_text(
            text = Language.get_prompt('language_set', self.language), 
            chat_id = self._chat_id, 
            message_id = msg_id
        )
        self._context = 'post_clip'
    
    def _save_clip(self) -> None:
        self._clip_service.save_clip(self._clip)

    def _send_message(self, prompt: str) -> None:
        self._bot.send_message(
            chat_id = self._chat_id, 
            text = View.get_prompt(prompt, self.language)
        )
    
    def start(self) -> None:
        self._send_message('start')
    
    def set_language(self) -> None:
        self._context = 'choose_language'
        self._bot.send_message(
            self._chat_id, 
            text = Language.get(self.language).get_prompt('choose_language'),
            reply_markup = View.get_language_reply_markup(),
            parse_mode = 'HTML'
        )

    def handle_clip_media(self, file_id: str) -> None:
        if self._clip.telegram_file_id is not None:
            self._send_message('media_updated')
        
        self._clip.telegram_file_id = file_id
        
        sleep(2)
        
        if self._clip.description is None:
            self._send_message('send_description')
        else:
            self._save_clip()

    def handle_message(self, text: str) -> None:
        match self._context:
            case 'post_clip':
                self._handle_clip_description(text)
            case 'report':
                self._handle_report_description(text)
    
    def handle_callback(self, data: Any, msg_id: int | str) -> None:
        match self._context:
            case 'choose_language':
                self._handle_set_language(data, msg_id)
            case _:
                raise TeleclipsException()
    


from .view import View
from .languages import Language
from .control import TeleBot
from .models import Clip
from .service import ClipService
from .errors import TeleclipsException, UnsupportedLanguageException, IncompleteClipSavingAttemptException