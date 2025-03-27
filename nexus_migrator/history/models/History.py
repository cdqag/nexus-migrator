from typing import Optional, List

from pydantic import BaseModel

from .HistoryEntry import HistoryEntry


class History(BaseModel):
    last_continuation_token: Optional[str] = None
    components: Optional[List[HistoryEntry]] = []
