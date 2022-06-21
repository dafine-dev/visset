from __future__ import annotations
from unittest import TestCase
from visset.models import MediaType, Clip


class TestModels(TestCase):

    def setUp(self) -> None:
        self.media_type = MediaType(code = 1, name = 'photo', strategy = lambda clip: True)
        self.clip = Clip(id = 1, description = 'description', telegram_file_id = 'asdgsr8fh7w8hqe7a', type = self.media_type)

    def test_to_inline(self) -> None:
        self.assertIs(self.media_type.to_inline(Clip()), True)

    def test_clip_serialize(self) -> None:
        self.assertListEqual(self.clip.serialize(), [1, 'description', 'asdgsr8fh7w8hqe7a', self.media_type])

    def test_clip_to_inline(self) -> None:
        self.assertIs(self.clip.to_inline(), True)
