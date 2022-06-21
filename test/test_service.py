from unittest import TestCase, mock
from visset.service import ClipService
from visset.models import Clip, MediaTypes
from visset.errors import IncompleteClipSavingAttemptException


class TestService(TestCase):

    def setUp(self) -> None:
        self.clip_sample = Clip(id = 1, description = 'example', telegram_file_id = 'asd5g7a8sr7aras7rf', type = MediaTypes.PHOTO)
        self.repository = mock.patch('visset.service.ClipRepository', spec = True).start()
        self.repository.return_value.select_by_description.return_value = [self.clip_sample]
        self.service = ClipService()

    def test_get_by_description(self) -> None:
        clips = self.service.get_by_description('example', wave = 1)
        self.assertListEqual(clips, [self.clip_sample])
        self.repository.return_value.select_by_description.assert_any_call('example', start = 0, limit = 10)

    def test_save_clip(self) -> None:
        clip = Clip(id = None, description = 'simple description', telegram_file_id = 's82dg7q8f78e5rfd74h8awef', type = MediaTypes.PHOTO)
        self.service.save_clip(clip)

    def test_save_incomplete_clip(self) -> None:
        clip = Clip()
        with self.assertRaises(IncompleteClipSavingAttemptException):
            self.service.save_clip(clip)

    def test_delete(self) -> None:
        self.service.delete(1)
