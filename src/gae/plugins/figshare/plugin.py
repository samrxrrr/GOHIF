from __future__ import annotations

from pathlib import Path

import requests

from gae.interfaces.plugin import AcquisitionPlugin


class FigsharePlugin(AcquisitionPlugin):

    @property
    def name(self):
        return "figshare"

    async def prepare(self, manifest):
        return None

    async def authenticate(self):
        return None

    async def acquire(self, manifest, destination: Path):

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        article = manifest.download.record_id

        api = f"https://api.figshare.com/v2/articles/{article}"

        r = requests.get(api, timeout=60)

        r.raise_for_status()

        metadata = r.json()

        files = metadata["files"]

        if len(files) == 0:
            raise RuntimeError("No downloadable files.")

        url = files[0]["download_url"]

        download = requests.get(
            url,
            stream=True,
            timeout=300,
        )

        download.raise_for_status()

        with open(destination, "wb") as output:

            for chunk in download.iter_content(
                1024 * 1024
            ):

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
