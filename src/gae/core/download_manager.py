from __future__ import annotations

from pathlib import Path

import requests

from gae.cache.cache import DownloadCache
from gae.config.settings import settings


class DownloadManager:

    def __init__(self):

        self.cache = DownloadCache(
            settings.cache_directory
        )

    def download(self, url: str, destination: Path):

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if self.cache.exists(url):

            print("[CACHE] HIT")

            self.cache.restore(
                url,
                destination,
            )

            return destination

        response = requests.get(
            url,
            stream=True,
            timeout=settings.timeout,
            verify=settings.verify_ssl,
        )

        response.raise_for_status()

        with open(destination, "wb") as output:

            for chunk in response.iter_content(
                settings.chunk_size
            ):

                if chunk:
                    output.write(chunk)

        self.cache.store(
            url,
            destination,
        )

        print("[CACHE] STORED")

        return destination
