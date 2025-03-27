from .Component import Component
from ..UploadPayload import UploadPayload


class PypiComponent(Component):

    def get_upload_payload(self) -> UploadPayload:
        payload = super().get_upload_payload()

        whl_file = None
        tar_gz_file = None

        for asset in self.assets:
            if asset.path.suffix == ".whl":
                if not asset.localPath:
                    raise Exception(
                        f"Asset {asset.path.name} was not downloaded")

                whl_file = asset.localPath

            elif asset.path.suffix == ".tar.gz":
                if not asset.localPath:
                    raise Exception(
                        f"Asset {asset.path.name} was not downloaded")

                tar_gz_file = asset.localPath

        if whl_file:
            payload.files["pypi.asset"] = open(whl_file, "rb")
        elif tar_gz_file:
            payload.files["pypi.asset"] = open(tar_gz_file, "rb")
        else:
            raise Exception("No WHL or TGZ file found in component")

        return payload
