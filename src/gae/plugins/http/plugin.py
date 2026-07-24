from pathlib import Path

import aiohttp

from gae.interfaces.plugin import AcquisitionPlugin


class HTTPPlugin(AcquisitionPlugin):

    @property
    def name(self) -> str:
        return "http"

    async def prepare(self, manifest):
        pass

    async def authenticate(self):
        pass

    async def acquire(self, manifest, destination: Path):

        async with aiohttp.ClientSession() as session:

            async with session.get(str(manifest.url)) as response:

                response.raise_for_status()

                with open(destination, "wb") as f:

                    while True:

                        chunk = await response.content.read(1024 * 1024)

                        if not chunk:
                            break

                        f.write(chunk)

        return destination

    async def verify(self, downloaded_file):
        return downloaded_file.exists()

    async def metadata(self, downloaded_file):

        return {
            "size": downloaded_file.stat().st_size
        }

    async def cleanup(self):
        pass
