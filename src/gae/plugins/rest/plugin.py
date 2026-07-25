from __future__ import annotations

from pathlib import Path

import requests

from gae.interfaces.plugin import AcquisitionPlugin


class RESTPlugin(AcquisitionPlugin):

    @property
    def name(self):
        return "rest"

    async def prepare(self, manifest):
        return None

    async def authenticate(self):
        return None

    async def acquire(self, manifest, destination: Path):

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        r = requests.get(
            manifest.download.url,
            timeout=300,
        )

        r.raise_for_status()

        destination.write_bytes(
            r.content
        )

        return destination

    async def verify(self, downloaded_file):

        return downloaded_file.exists()

    async def metadata(self, downloaded_file):

        return {
            "size": downloaded_file.stat().st_size
        }

    async def cleanup(self):
        return None
