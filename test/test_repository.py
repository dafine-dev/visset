from unittest import TestCase, mock
from visset.repository import ClipRepository
from visset.models import Clip, MediaType, MediaTypes


class TestRepository(TestCase):

    def setUp(self) -> None:
        self.repository = ClipRepository()
        self.connection = mock.patch('visset.repository.Connection').start()
        self.connection.return_value.__enter__.return_value \
            .get_result.return_value = [{'id': 1, 'description': 'description', 'telegram_file_id': 'sda4sda7s8d', 'type': 1}]

    def test_build_select(self):
        sql = self.repository._build_select(description = 'simple description', start = 0, limit = 10)
        assert sql == 'select id, description, telegram_file_id, type from Clip where description like 0x2573696d706c65206465736372697074696f6e25 limit 0, 10;'

    def test_build_insert(self):
        clip = Clip(
            id = 1,
            description = 'simple description',
            telegram_file_id = '34as8d4as35d4a',
            type = MediaType(1, '', None)
        )

        sql = 'insert into Clip (id, description, telegram_file_id, type) values ' \
            + '(default, 0x73696d706c65206465736372697074696f6e, 0x3334617338643461733335643461, 1);'
        assert self.repository._build_insert(clip) == sql

    def test_build_delete(self):
        assert self.repository._build_delete(1) == 'delete from Clip where id = 1;'

    def test_from_dictionary(self):
        clip = self.repository._from_dictionary({'id': 1, 'description': 'description', 'telegram_file_id': 'hjrh5s4r87AErWAQ', 'type': 4})
        self.assertEqual(clip, Clip(1, 'description', 'hjrh5s4r87AErWAQ', MediaTypes.STICKER.value))

    def test_insert(self):
        self.repository.insert(
            Clip(None, 'simple description', 'as4d8as74da53sdf4a', MediaType(code = 1, name = None, strategy = None))
        )

    def test_delete(self):
        self.repository.delete(1)

    def test_select(self):
        clips = self.repository.select_by_description('simple description', start = 1, limit = 10)
        self.assertListEqual(clips, [Clip(1, 'description', 'sda4sda7s8d', MediaTypes.PHOTO.value)])

    def tearDown(self) -> None:
        self.connection.stop()
