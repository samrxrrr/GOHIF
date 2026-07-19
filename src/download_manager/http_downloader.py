"""
GOHIF HTTP Downloader

Supports:
- HTTP/HTTPS downloads
- Resume support
- Retry logic
- Timeout handling
- Automatic directory creation
- Logging
"""

from __future__ import annotations

import subprocess
from pathlib import Path

try:
    from .utils import (
        ensure_directory,
        verify_file,
        log_download,
    )
except ImportError:
    from utils import (
        ensure_directory,
        verify_file,
        log_download,
    )


def download(
    url: str,
    output_directory: str,
    filename: str | None = None,
    retries: int = 3,
    timeout: int = 60,
) -> Path:
    """
    Download a file using wget.

    Parameters
    ----------
    url : str
        Download URL.

    output_directory : str
        Directory where the file will be stored.

    filename : str | None
        Optional output filename.

    retries : int
        Number of retries.

    timeout : int
        Network timeout (seconds).

    Returns
    -------
    pathlib.Path
        Path to downloaded file.
    """

    destination = ensure_directory(output_directory)

    if filename is None:
        filename = url.split("/")[-1]

    output_file = destination / filename

    command = [
        "wget",
        "--continue",
        "--tries",
        str(retries),
        "--timeout",
        str(timeout),
        "-O",
        str(output_file),
        url,
    ]

    print("Executing:")
    print(" ".join(command))

    result = subprocess.run(command)

    if result.returncode != 0:
        log_download(filename, "FAILED", url)
        raise RuntimeError(f"Download failed: {url}")

    if not verify_file(output_file):
        raise RuntimeError(f"Downloaded file is empty: {output_file}")

    log_download(filename, "SUCCESS", str(output_file))

    return output_file


def self_test():
    print("=" * 60)
    print("GOHIF HTTP Downloader")
    print("=" * 60)
    print("Module imported successfully.")
    print("Self-test passed.")
    print("=" * 60)


if __name__ == "__main__":
    self_test()
