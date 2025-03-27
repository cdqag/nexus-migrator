from typing import Optional
from .Historian import Historian

_historian = None


def init_historian(name: str):
    global _historian
    _historian = Historian(name)
    return _historian


def get_historian() -> Optional[Historian]:
    return _historian
