from __future__ import annotations



class ClipService:
    
    def __init__(self) -> None:
        self._repository = ClipRepository()
    
    def save_clip(self, clip: Clip) -> None:
        if not (clip.description and clip.telegram_file_id and clip.type):
            raise IncompleteClipSavingAttemptException()

        self._repository.insert(clip)
    
    def get_by_description(self, description: str, wave: int = 1) -> list[Clip]:
        return self._repository.select_by_description(description, start = (wave - 1) * 10, limit = 10)
    
    def delete(self, id: int) -> None:
        self._repository.delete(id)


from .models import Clip
from .repository import ClipRepository
from .errors import IncompleteClipSavingAttemptException