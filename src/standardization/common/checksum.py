"""
GOHIF Checksum Utilities

Shared hashing functions used by all parsers.
"""

import hashlib
from pathlib import Path


def sha256(path, chunk_size=1024 * 1024):
    """
    Calculate SHA256 checksum.

    Parameters
    ----------
    path : str or Path

    chunk_size : int

    Returns
    -------
    str
    """

    path = Path(path)

    hasher = hashlib.sha256()

    with open(path, "rb") as handle:

        while True:

            chunk = handle.read(chunk_size)

            if not chunk:
                break

            hasher.update(chunk)

    return hasher.hexdigest()


def md5(path, chunk_size=1024 * 1024):
    """
    Calculate MD5 checksum.
    """

    path = Path(path)

    hasher = hashlib.md5()

    with open(path, "rb") as handle:

        while True:

            chunk = handle.read(chunk_size)

            if not chunk:
                break

            hasher.update(chunk)

    return hasher.hexdigest()
