from __future__ import annotations
from mysql import connector
from typing import Any
from .utils import singleton


@singleton
class Connection:

    def __init__(self) -> None:
        self._conn = ...
        self._cursor = ...

    def __enter__(self) -> Connection:
        self._conn = connector.connect(option_files = 'application.conf', option_groups = 'connection')
        self._cursor = self._conn.cursor(dictionary = True)
        return self

    def __exit__(self, type, value, traceback) -> bool:
        if isinstance(value, connector.Error):
            raise DatabaseTransactionException()
        self.close()

    def execute(self, sql: str) -> None:
        print(sql)
        self._cursor.execute(sql)

    def commit(self) -> None:
        self._conn.commit()

    def get_result(self) -> list[dict[str, Any]]:
        return self._cursor.fetchall()

    def close(self) -> None:
        self._conn.close()
        self._conn = ...
        self._cursor = ...


class ClipRepository:

    def insert(self, clip: Clip) -> None:
        with Connection() as conn:
            conn.execute(self._build_insert(clip))
            conn.commit()

    def select_by_description(self, description: str, start: int = 0, limit: int = 10) -> list[Clip]:
        sql = self._build_select(description, start, limit)
        with Connection() as conn:
            conn.execute(sql)
            result = [self._from_dictionary(d) for d in conn.get_result()]

        return result

    def delete(self, id: int) -> None:
        with Connection() as conn:
            conn.execute(self._build_delete(id))
            conn.commit()

    def _from_dictionary(self, dictionary: dict[str, Any]) -> Clip:
        types = list(MediaTypes)
        return Clip(dictionary['id'], dictionary['description'], dictionary['telegram_file_id'], types[dictionary['type'] - 1].value)

    def _build_select(self, description: str, start: int, limit: int) -> str:
        return (
            'select '
            + 'id, description, telegram_file_id, type '
            + 'from '
            + 'Clip '
            + 'where '
            + f'description like 0x{f"%{description}%".encode("utf-8").hex()} limit {start}, {limit};'
        )

    def _build_insert(self, clip: Clip) -> str:
        return (
            'insert into Clip '
            + '(id, description, telegram_file_id, type) values '
            + f'(default, 0x{clip.description.encode("utf-8").hex()}, 0x{clip.telegram_file_id.encode("utf-8").hex()}, {clip.type});'
        )

    def _build_delete(self, id: int) -> str:
        return (
            f'delete from Clip where id = {id};'
        )


from .errors import DatabaseTransactionException
from .models import Clip, MediaTypes
