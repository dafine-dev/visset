from __future__ import annotations
from .session import ChatSession, Session, UserSession
from telebot import TeleBot
from telebot import types


bot = TeleBot()
Message = types.Message

Session.start_bot(bot)


@bot.message_handler(commands = ['start'])
def handle_start(msg: Message):
    with ChatSession(id = msg.chat.id) as session:
        session.start()


@bot.message_handler(commands = ['set_language'])
def handle_set_language(msg: Message):
    with ChatSession(id = msg.chat.id) as session:
        session.set_language()


@bot.callback_query_handler
def handle_callbacks(call: types.CallbackQuery):
    with ChatSession(id = call.message.chat.id) as session:
        data = call.data
        msg_id = call.message.id

        session.handle_callback(data, msg_id)


@bot.message_handler(content_types = ['photo'])
def on_photos(msg: Message):
    with ChatSession(id = msg.chat.id) as session:
        session.handle_clip_media(file_id = msg.photo[-1].file_id)


@bot.message_handler(content_types = ['video'])
def on_videos(msg: Message):
    with ChatSession(id = msg.chat.id) as session:
        session.handle_clip_media(file_id = msg.video.file_id)


@bot.message_handler(content_types = ['animation'])
def on_gifs(msg: Message):
    with ChatSession(id = msg.chat.id) as session:
        session.handle_clip_media(file_id = msg.animation.file_id)


@bot.message_handler(content_types = ['sticker'])
def on_stickers(msg: Message):
    with ChatSession(id = msg.chat.id) as session:
        session.handle_clip_media(file_id = msg.sticker.file_id)


@bot.message_handler(content_types = ['text'])
def on_message(msg: Message):
    with ChatSession(id = msg.chat.id) as session:
        session.handle_message(text = msg.text)


@bot.inline_handler
def on_inline_query(inline_query: types.InlineQuery):
    user_id = inline_query.from_user.id
    query_id = inline_query.id
    query = inline_query.query

    with UserSession(id = user_id) as session:
        session.handle_inline_query(query_id, query)
