from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class HistoryEntry(BaseModel):
    id: str
    last_downloaded: Optional[datetime] = None
    has_been_skipped: Optional[bool] = False
    skip_reason: Optional[str] = None
    has_been_migrated: Optional[bool] = False
