from __future__ import annotations

from pathlib import Path

import requests

from gae.interfaces.plugin import AcquisitionPlugin


class ZenodoPlugin(AcquisitionPlugin):

    @property
    def name(self):
        return "zenodo"

    async def prepare(self, manifest):
        return None

    async def authenticate(self):
        return None

    async def acquire(self, manifest, destination: Path):

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        record_id = manifest.download.record_id

        api = f"https://zenodo.org/api/records/{record_id}"

        response = requests.get(api, timeout=60)
        response.raise_for_status()

        metadata = response.json()

        files = metadata.get("files", [])

        if not files:
            raise RuntimeError("No downloadable files found.")

        file_url = files[0]["links"]["self"]

        r = requests.get(file_url, stream=True, timeout=300)
        r.raise_for_status()

        with open(destination, "wb") as output:

            for chunk in r.iter_content(1024 * 1024):

                if chunk:
                    output.write(chunk)

        return destination

    async def verify(self, downloaded_file):

        return downloaded_file.exists()

    async def metadata(self, downloaded_file):

        return {
            "size": downloaded_file.stat().st_size
        }

    async def cleanup(self):
        return None
