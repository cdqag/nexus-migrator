from .Component import Component
from ..UploadPayload import UploadPayload


class RawComponent(Component):
    group: str

    def __str__(self):
        return f"{self.name} ({self.id})"

    def get_upload_payload(self) -> UploadPayload:
        payload = super().get_upload_payload()

        i = 1
        for asset in self.assets:
            if not asset.localPath:
                raise Exception(
                    f"Asset {asset.path.name} was not downloaded")

            payload.files[f"raw.asset{i}"] = open(asset.localPath, "rb")
            payload.data[f"raw.asset{i}.filename"] = asset.path.name
            i += 1

            if i > 3:
                print("Warning: Only the first 3 assets will be uploaded")
                break

        payload.data["raw.directory"] = self.group
        return payload
