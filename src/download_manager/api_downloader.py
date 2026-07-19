"""
GOHIF API Downloader

Supports:
- ENA Portal API
- MGnify API
- Generic REST APIs
"""

from __future__ import annotations

import requests
from pathlib import Path

try:
    from .utils import (
        ensure_directory,
        log_download,
        verify_file,
    )
except ImportError:
    from utils import (
        ensure_directory,
        log_download,
        verify_file,
    )


class APIDownloader:

    def __init__(self, timeout: int = 60):
        self.timeout = timeout

    def download_file(
        self,
        url: str,
        output_directory: str,
        filename: str,
    ) -> Path:

        output_dir = ensure_directory(output_directory)
        output_file = output_dir / filename

        print(f"Downloading: {url}")

        response = requests.get(url, stream=True, timeout=self.timeout)
        response.raise_for_status()

        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        if not verify_file(output_file):
            raise RuntimeError("Downloaded file is empty.")

        log_download(filename, "SUCCESS", str(output_file))

        return output_file

    def get_json(self, url: str):

        print(f"Requesting JSON: {url}")

        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()

        return response.json()


def self_test():

    print("=" * 60)
    print("GOHIF API Downloader")
    print("=" * 60)

    response = requests.get(
        "https://httpbin.org/get",
        timeout=30,
    )

    print("HTTP Status :", response.status_code)
    print("Connectivity :", "PASS")

    print("=" * 60)


if __name__ == "__main__":
    self_test()
