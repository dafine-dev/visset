from __future__ import annotations
import json
from typing import Iterable


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

    @classmethod
    def start(cls) -> None:
        for language_info in json.load(open('prompts.json', 'r', encoding='utf-8')):
            cls.create(**language_info)

    def get_prompt(self, prompt_name: str) -> str:
        return self._prompts[prompt_name]
