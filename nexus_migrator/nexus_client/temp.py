from pathlib import Path
from tempfile import gettempdir

temp_dir = Path(gettempdir()) / "nexus_migrator"
temp_dir.mkdir(parents=True, exist_ok=True)
