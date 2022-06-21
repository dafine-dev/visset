from __future__ import annotations
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import InlineQueryResultCachedBase


class View:

    @classmethod
    def get_language_reply_markup(cls) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()

        for language in Language.get_all():
            keyboard.add(InlineKeyboardButton(text = language.view_name, callback_data = language.inner_name))

        return keyboard

    @classmethod
    def get_clips_inline_answer(cls, clips: list[Clip]) -> list[InlineQueryResultCachedBase]:
        return [clip.to_inline() for clip in clips]


from .languages import Language
from .models import Clip
