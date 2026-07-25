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

        record = manifest.download.record_id

        api = f"https://zenodo.org/api/records/{record}"

        metadata = requests.get(api).json()

        file_url = metadata["files"][0]["links"]["self"]

        r = requests.get(file_url)

        destination.write_bytes(r.content)

        return destination

    async def verify(self, downloaded_file):
        return downloaded_file.exists()

    async def metadata(self, downloaded_file):
        return {
            "size": downloaded_file.stat().st_size
        }

    async def cleanup(self):
        return None
