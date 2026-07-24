from __future__ import annotations

from pathlib import Path

import aiohttp

from gae.download.checksum import verify_checksum
from gae.interfaces.plugin import AcquisitionPlugin


class HTTPPlugin(AcquisitionPlugin):

    @property
    def name(self) -> str:
        return "http"

    async def prepare(self, manifest):
        return None

    async def authenticate(self):
        return None

    async def acquire(self, manifest, destination: Path):

        async with aiohttp.ClientSession() as session:

            async with session.get(str(manifest.download.url)) as response:

                response.raise_for_status()

                with destination.open("wb") as output:

                    async for chunk in response.content.iter_chunked(1024 * 1024):
                        output.write(chunk)

        return destination

    async def verify(self, downloaded_file: Path):

        return downloaded_file.exists()

    async def metadata(self, downloaded_file: Path):

        metadata = {
            "size": downloaded_file.stat().st_size,
        }

        return metadata

    async def cleanup(self):
        return None
