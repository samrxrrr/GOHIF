from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import aioftp

from gae.interfaces.plugin import AcquisitionPlugin


class FTPPlugin(AcquisitionPlugin):

    @property
    def name(self):
        return "ftp"

    async def prepare(self, manifest):
        return None

    async def authenticate(self):
        return None

    async def acquire(self, manifest, destination: Path):

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        parsed = urlparse(str(manifest.download.url))

        host = parsed.hostname

        remote = parsed.path

        async with aioftp.Client.context(
            host,
            port=21,
        ) as client:

            await client.download(
                remote,
                destination,
                write_into=True,
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
