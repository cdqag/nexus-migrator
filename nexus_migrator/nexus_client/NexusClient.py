from datetime import datetime, timedelta

import httpx
from httpx_retries import RetryTransport, Retry

from .factory import factory_component
from .models.Component import Component
from ..history import get_historian

HTTP_TIMEOUT = 600  # seconds


class NexusClient:

    def __init__(self, base_url: str, username: str, password: str):
        basic_auth = httpx.BasicAuth(username=username, password=password)

        base_service_url = httpx.URL(base_url, path="/service/rest/v1")

        retry = Retry(total=3, backoff_factor=10)
        transport = RetryTransport(retry=retry)

        self.rest_api = httpx.Client(base_url=base_service_url, auth=basic_auth, transport=transport)

    def list_components(self, repository: str, downloaded_in_days: int = 0):
        due_date = None
        if downloaded_in_days > 0:
            due_date = datetime.now() - timedelta(days=downloaded_in_days)

        page = 1
        continuation_token = None
        historian = get_historian()
        if historian:
            continuation_token = historian.get_last_continuation_token()

        while True:
            params = {"repository": repository}
            if continuation_token:
                params["continuationToken"] = continuation_token
                if historian:
                    historian.note_last_continuation_token(continuation_token)

            # typer.echo(f"Getting components from page {page}...")
            res = self.rest_api.get("components", params=params, timeout=HTTP_TIMEOUT)

            data = res.json()
            for item in data["items"]:
                try:
                    component = factory_component(item)

                except Exception as e:
                    if historian:
                        historian.note_component(item["id"],
                                              skip_reason=str(e))
                    continue

                # Return none if the component was not downloaded in the last N days
                if due_date:
                    to_compare = [asset.lastDownloaded for asset in component.assets if asset.lastDownloaded]
                    if len(to_compare) == 0:
                        if historian:
                            historian.note_component(item["id"], skip_reason="No download date")
                        continue
                    last_downloaded = max(to_compare)
                    if historian:
                        historian.note_component(item["id"], last_downloaded=last_downloaded)
                    if last_downloaded.timestamp() < due_date.timestamp():
                        if historian:
                            historian.note_component(item["id"], skip_reason=f"Not downloaded in the last {downloaded_in_days} days")
                        continue

                yield component

            if "continuationToken" in data and data["continuationToken"]:
                continuation_token = data["continuationToken"]
                page += 1
                continue
            break

    def download_component(self, component: Component):
        component.download(self)

    def upload_component(self, component: Component, repository: str):
        payload = component.get_upload_payload()

        params = {"repository": repository}
        res = self.rest_api.post("components", params=params, data=payload.data, files=payload.files, timeout=HTTP_TIMEOUT)

        if res.status_code != 204:
            raise Exception(f"Error uploading component: {res.text}")
