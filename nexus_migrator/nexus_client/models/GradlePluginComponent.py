from .Component import Component
from .ComponentAsset import ComponentAsset
from ..UploadPayload import UploadPayload


class GradlePluginComponent(Component):
    group: str

    def __str__(self):
        return f"{self.group}:{self.name}:{self.version} ({self.id})"

    def should_download_asset(self, asset: ComponentAsset) -> bool:
        if not super().should_download_asset(asset):
            return False

        if asset.path.suffix == ".pom":
            return True

        return False

    def get_upload_payload(self) -> UploadPayload:
        payload = super().get_upload_payload()

        if self.version:
            payload.data["version"] = self.version

        payload.data["maven2.groupId"] = self.group
        payload.data["maven2.artifactId"] = self.name
        payload.data["maven2.packaging"] = "pom"

        pom_file = None

        for asset in self.assets:
            if asset.path.suffix == ".pom":
                if not asset.localPath:
                    raise Exception(
                        f"Asset {asset.path.name} was not downloaded")

                pom_file = asset.localPath

        payload.files["maven2.asset1"] = open(pom_file, "rb")
        payload.data["maven2.asset1.extension"] = "pom"
        payload.data["maven2.generate-pom"] = "false"

        return payload
