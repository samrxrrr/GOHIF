from __future__ import annotations

from pathlib import Path

import aiohttp

from gae.core.retry import retry_policy
from gae.interfaces.plugin import AcquisitionPlugin


class HTTPPlugin(AcquisitionPlugin):

    @property
    def name(self):
        return "http"

    async def prepare(self, manifest):
        return None

    async def authenticate(self):
        return None

    @retry_policy()
    async def acquire(self, manifest, destination: Path):

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        downloaded = 0

        headers = {}

        mode = "wb"

        if destination.exists():

            downloaded = destination.stat().st_size

            if downloaded > 0:
                headers["Range"] = f"bytes={downloaded}-"
                mode = "ab"

        timeout = aiohttp.ClientTimeout(total=None)

        async with aiohttp.ClientSession(
            timeout=timeout
        ) as session:

            async with session.get(
                str(manifest.download.url),
                headers=headers,
            ) as response:

                if response.status not in (200,206):
                    response.raise_for_status()

                with open(destination,mode) as output:

                    async for chunk in response.content.iter_chunked(
                        1024*1024
                    ):
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
