from __future__ import annotations
from dataclasses import dataclass


@dataclass(slots = True)
class Clip:
    id: int
    description: str
    telegram_file_id: str
    type: int

    def serialize(self) -> list[int, str, str, int]:
        return [self.id, self.description, self.telegram_file_id, self.type]
