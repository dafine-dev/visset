from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Callable
from telebot import types
from enum import Enum


@dataclass(slots=True)
class Clip:
    id: int = None
    description: str = None
    telegram_file_id: str = None
    type: MediaType = None

    def serialize(self) -> list[int, str, str, int]:
        return [self.id, self.description, self.telegram_file_id, self.type]

    def from_message(self, msg: types.Message) -> None:
        self.type = MediaTypes[msg.content_type].value

        media = getattr(msg, msg.content_type)
        media = media[-1] if isinstance(media, (list, tuple)) else media

        self.telegram_file_id = media.file_id

    def to_inline(self) -> types.InlineQueryResultCachedBase:
        return self.type.to_inline(self)


class MediaType:
    _code: int
    _name: str
    _strategy: inline_strategy

    def __init__(self, code: int, name: str, strategy: inline_strategy) -> None:
        self._code = code
        self._name = name
        self._strategy = strategy

    def __str__(self) -> str:
        return str(self._code)

    def to_inline(self, clip: Clip) -> types.InlineQueryResultCachedBase:
        return self._strategy(clip)


inline_strategy = Callable[[MediaType, Clip], types.InlineQueryResultCachedBase]


class MediaTypes(Enum):
    value: MediaType
    PHOTO = MediaType(
        code = 1,
        name = 'photo',
        strategy = lambda clip: types.InlineQueryResultCachedPhoto(
            id = clip.id,
            photo_file_id = clip.telegram_file_id,
            title = clip.description
        )
    )

    VIDEO = MediaType(
        code = 2,
        name = 'video',
        strategy = lambda clip: types.InlineQueryResultCachedVideo(
            id = clip.id,
            video_file_id = clip.telegram_file_id,
            title = clip.description
        )
    )

    GIF = MediaType(
        code = 3,
        name = 'animation',
        strategy = lambda clip: types.InlineQueryResultCachedGif(
            id = clip.id,
            gif_file_id = clip.telegram_file_id,
            title = clip.description
        )
    )

    STICKER = MediaType(
        code = 4,
        name = 'sticker',
        strategy = lambda clip: types.InlineQueryResultCachedSticker(
            id = clip.id,
            sticker_file_id = clip.telegram_file_id,
        )
    )

    photo = PHOTO
    video = VIDEO
    animation = GIF
    sticker = STICKER
