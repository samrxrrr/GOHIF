from __future__ import annotations

import shutil
from pathlib import Path

import requests

from gae.cache.cache import DownloadCache


class DownloadManager:

    def __init__(self):

        self.cache = DownloadCache(
            Path.home() / ".gae_cache"
        )

    def download(self, url: str, destination: Path):

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if self.cache.exists(url):

            print("[CACHE] Using cached copy")

            self.cache.restore(
                url,
                destination,
            )

            return destination

        response = requests.get(
            url,
            stream=True,
            timeout=300,
        )

        response.raise_for_status()

        with open(destination, "wb") as output:

            for chunk in response.iter_content(
                1024 * 1024
            ):

                if chunk:

                    output.write(chunk)

        self.cache.store(
            url,
            destination,
        )

        print("[CACHE] Stored download")

        return destination
