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
        self._conn = connector.connect(option_files = 'connection.conf', option_groups = 'connection')
        self._cursor = self._conn.cursor(dictionary = True)
        return self

    def __exit__(self, type, value, traceback) -> bool:
        self.close()
    
    def execute(self, sql: str) -> None:
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
        sql = 'insert into Clip(id, description, telegram_file_id, type) values (%d, 0x%d, %d, %d);'

        with Connection() as conn:
            conn.execute(sql % self._from_clip(clip))
            conn.commit()
        
    def select_by_description(self, description: str, start: int = 0, limit: int = 10) -> list[Clip]:
        sql = f'select id, description, telegram_file_id, type from Clip where description ilike 0x{description.encode("utf-8").hex()} limit {start}, {limit};'
        with Connection() as conn:
            conn.execute(sql)
            result = [self._from_dictionary(d) for d in conn.get_result()]

        return result
    
    def delete(self, id: int) -> None:
        sql = f'delete from Clip where id = {id}'
        with Connection() as conn:
            conn.execute(sql)
            conn.commit()

    def _from_dictionary(self, dictionary: dict[str, Any]) -> Clip:
        return Clip(**dictionary)
    
    def _from_clip(self, clip: Clip) -> tuple[int, str, str, int]:
        values = clip.serialize()
        values[1] = values[1].encode('utf-8').hex()
        return values


from .models import Clip