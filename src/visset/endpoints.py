from __future__ import annotations
from __main__ import bot
from telebot import types


content_types = [
    'audio',
    'animation',
    'document',
    'photo',
    'sticker',
    'video',
    'video_note',
    'voice',
    'location',
    'contact'
]


@bot.message_handler(commands = ['start'])
def handle_start(msg: types.Message):
    with Controller() as controller:
        controller.handle_start(msg)


@bot.message_handler(commands = ['set_language'])
def handle_set_language(msg: types.Message):
    with Controller() as controller:
        controller.handle_set_language(msg)


@bot.message_handler(commands = ['cancel'])
def handle_cancel(msg: types.Message):
    with Controller() as controller:
        controller.handle_cancel(msg)


@bot.callback_query_handler(func = lambda _: True)
def handle_callback(callback: types.CallbackQuery):
    with Controller() as controller:
        controller.handle_callback(callback)


@bot.message_handler(content_types = content_types)
def handle_media(msg: types.Message):
    with Controller() as controller:
        controller.handle_media(msg)


@bot.message_handler(func = lambda _: True)
def handle_message(msg: types.Message):
    with Controller() as controller:
        controller.handle_message(msg)


@bot.inline_handler(func = lambda _: True)
def handle_inline(inline_query: types.InlineQuery):
    with Controller() as controller:
        controller.handle_inline_query(inline_query)


from .controllers import Controller
