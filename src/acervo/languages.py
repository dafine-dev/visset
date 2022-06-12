from __future__ import annotations
from typing import Iterable

_english: dict[str, str] = {
    'start' : 'To start, send a description or a media (photo, video, gif, sticker) or both to save.',
    'send_description' : 'Send a message with the description to this media.',
    'send_media' : 'Send the media (photo, video, gif, sticker) descripted by the message.',
    'description_updated' : 'Description updated!',
    'media_updated' : 'Media Updated!',
    'choose_language' : 'Chose language:',
    'language_set' : 'Language updated!',
    'invalid_language' : 'Choosen language is not supported.',
    'incomplete_clip_error' : 'Can not save a clip with no media or description.',
}

_portuguese: dict[str, str] = {
    'start' : 'Para começar, envie uma descrição ou mídia (foto, vídeo, gif, figurinha) ou ambos para salvar.',
    'send_description' : 'Envie uma mensagem com a descrição para essa mídia.',
    'send_media' : 'Envie a mídia (foto, vídeo, gif, figurinha) descrita pela mensagem.',
    'description_updated' : 'Descrição alterada!',
    'media_updated' : 'Mídia alterada!',
    'choose_language' : 'Escolha um idioma:',
    'language_set' : 'Idioma alterado!',
    'invalid_language' : 'Idioma escolhido não disponível.',
    'incomplete_clip_error' : 'Não é possível salvar clip sem mídia ou descrição.'
}


class Language:
    view_name: str
    inner_name: str
    _prompts: dict[str, str]
    _instances: dict[str, Language] = {}

    def __init__(self, inner_name: str, view_name: str, prompts: dict[str, str]) -> None:
        self.inner_name = inner_name
        self.view_name = view_name
        self._prompts = prompts

    @classmethod
    def create(cls, inner_name: str, view_name: str, prompts: dict[str, str]) -> Language:
        language = Language(inner_name, view_name, prompts)
        cls._instances[inner_name] = language
        return language
    
    @classmethod
    def get_all(cls) -> Iterable[Language]:
        return cls._instances.values()

    @classmethod
    def get(cls, name: str) -> Language:
        return cls._instances[name]
    
    @classmethod
    def validate(self, name: str) -> bool:
        return name in self._instances

    def get_prompt(self, prompt_name: str) -> str:
        return self._prompts[prompt_name]


Language.create('portuguese', 'Portuguese 🇧🇷', _portuguese)
Language.create('english', 'English 🇺🇸', _english)