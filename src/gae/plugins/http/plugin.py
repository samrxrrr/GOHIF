from __future__ import annotations

from pathlib import Path

import aiohttp

from gae.core.retry import retry_policy
from gae.interfaces.plugin import AcquisitionPlugin


class HTTPPlugin(AcquisitionPlugin):

    @property
    def name(self) -> str:
        return "http"

    async def prepare(self, manifest):
        return None

    async def authenticate(self):
        return None

    @retry_policy()
    async def acquire(
        self,
        manifest,
        destination: Path,
    ):

        timeout = aiohttp.ClientTimeout(
            total=300,
        )

        async with aiohttp.ClientSession(
            timeout=timeout,
        ) as session:

            async with session.get(
                str(manifest.download.url)
            ) as response:

                response.raise_for_status()

                with destination.open("wb") as output:

                    async for chunk in response.content.iter_chunked(
                        1024 * 1024
                    ):
                        output.write(chunk)

        return destination

    async def verify(
        self,
        downloaded_file: Path,
    ):
        return downloaded_file.exists()

    async def metadata(
        self,
        downloaded_file: Path,
    ):

        return {
            "size": downloaded_file.stat().st_size
        }

    async def cleanup(self):
        return None
