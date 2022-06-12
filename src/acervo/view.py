from __future__ import annotations
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton


class View:
    
    @classmethod
    def get_language_reply_markup(cls) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(text = language.view_name, callback_data = language.inner_name) for language in Language.get_all()
        )


from .languages import Language