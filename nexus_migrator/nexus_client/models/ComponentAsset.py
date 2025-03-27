from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class ComponentAsset(BaseModel):
    downloadUrl: str
    path: Path
    lastDownloaded: Optional[datetime] = None
    localPath: Optional[Path] = None
