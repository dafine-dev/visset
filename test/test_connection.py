from visset.repository import Connection, connector
from visset.errors import DatabaseTransactionException
from unittest import TestCase, mock


class TestConnection(TestCase):

    def setUp(self) -> None:
        self.result = [{'id': None, 'description': None, 'telegram_file_id': None, 'type': None}]
        self.db_connection = mock.patch('mysql.connector.connect').start()

    def test_connection(self) -> None:
        with Connection():
            ...

    def test_get_result(self) -> None:
        self.db_connection.return_value \
            .cursor.return_value \
            .fetchall.return_value = self.result
        with Connection() as conn:
            self.assertListEqual(conn.get_result(), self.result)

    def test_commit(self) -> None:
        with Connection() as conn:
            conn.commit()

    def test_commit_error(self) -> None:
        with self.assertRaises(AttributeError):
            Connection().commit()

    def test_close_error(self) -> None:
        with self.assertRaises(AttributeError):
            Connection().close()

    def test_connection_error(self) -> None:
        self.db_connection.return_value \
            .cursor.return_value \
            .execute.side_effect = connector.Error
        with self.assertRaises(DatabaseTransactionException):
            with Connection() as conn:
                conn.execute('select * from Clip')

    def tearDown(self) -> None:
        self.db_connection.stop()
