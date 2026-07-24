from __future__ import annotations

import hashlib
from pathlib import Path


def calculate_checksum(
    file_path: Path,
    algorithm: str = "sha256",
    chunk_size: int = 1024 * 1024,
) -> str:
    hasher = hashlib.new(algorithm)

    with file_path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)

    return hasher.hexdigest()


def verify_checksum(
    file_path: Path,
    algorithm: str,
    expected: str,
) -> bool:
    actual = calculate_checksum(
        file_path=file_path,
        algorithm=algorithm,
    )

    return actual.lower() == expected.lower()
