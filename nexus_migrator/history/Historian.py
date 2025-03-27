from datetime import datetime
from pathlib import Path
import json
from typing import Optional

from .models.History import History
from .models.HistoryEntry import HistoryEntry


class Historian:

    def __init__(self, name: str):
        self._file = Path(f"history-{name}.json")
        self._history: History = History()

        if self._file.exists():
            with self._file.open() as f:
                try:
                    loaded_history = json.load(f)
                except json.JSONDecodeError:
                    pass

            self._history = History(**loaded_history)

    def get_component_note_idx(self, component_id: str) -> int:
        for idx, entry in enumerate(self._history.components):
            if entry.id == component_id:
                return idx
        return -1

    def has_component_been_migrated(self, component_id: str) -> bool:
        entry_idx = self.get_component_note_idx(component_id)
        if entry_idx == -1:
            return False
        return self._history.components[entry_idx].has_been_migrated

    def note_component(self,
             _id: str,
             last_downloaded: Optional[datetime] = None,
             skip_reason: Optional[str] = None,
             has_been_migrated: Optional[bool] = None):

        entry_idx = self.get_component_note_idx(_id)
        if entry_idx != -1:
            entry = self._history.components[entry_idx]
        else:
            entry = HistoryEntry(id=_id)

        if last_downloaded is not None:
            entry.last_downloaded = last_downloaded

        if skip_reason is not None:
            entry.has_been_skipped = True
            entry.skip_reason = skip_reason

        elif has_been_migrated is not None:
            entry.has_been_migrated = has_been_migrated

        if entry_idx == -1:
            self._history.components.append(entry)

        self.save()

    def note_last_continuation_token(self, token: str):
        self._history.last_continuation_token = token
        self.save()

    def get_last_continuation_token(self) -> Optional[str]:
        return self._history.last_continuation_token

    def save(self):
        with self._file.open("w") as f:
            f.write(self._history.model_dump_json(indent=2))
