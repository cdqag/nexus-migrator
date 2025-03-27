from pathlib import Path
import shutil
from typing import Optional, List

from pydantic import BaseModel

from .ComponentAsset import ComponentAsset
from ..UploadPayload import UploadPayload
from ..temp import temp_dir


class Component(BaseModel):
    id: str
    name: str
    version: Optional[str] = None
    assets: Optional[List[ComponentAsset]] = []

    def __str__(self):
        return f"{self.name}:{self.version} ({self.id})"

    def get_temp_dir_path(self) -> Path:
        return temp_dir / self.id

    def get_temp_dir(self) -> Path:
        _dir = self.get_temp_dir_path()
        _dir.mkdir(parents=True, exist_ok=True)
        return _dir

    def remove_temp_dir(self):
        shutil.rmtree(self.get_temp_dir_path())

    def is_downloaded(self) -> bool:
        if not self.get_temp_dir_path().exists():
            return False

        for asset in self.assets:
            asset_path = self.get_temp_dir() / asset.path.name
            if not asset_path.exists():
                return False

        return True

    def should_download_asset(self, asset: ComponentAsset) -> bool:
        if not asset.localPath:
            return True

        if not asset.localPath.exists():
            return True

        return False

    def download(self, nexus_client):
        for asset in self.assets:
            if not self.should_download_asset(asset):
                continue

            res = nexus_client.rest_api.get(asset.downloadUrl)

            asset_temp_path = self.get_temp_dir() / asset.path.name

            with open(asset_temp_path, "wb") as f:
                f.write(res.content)
                asset.localPath = asset_temp_path

    def get_upload_payload(self) -> UploadPayload:
        data = {}
        files = {}

        return UploadPayload(data, files)
