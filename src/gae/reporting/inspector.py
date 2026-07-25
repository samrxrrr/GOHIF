from __future__ import annotations

from pathlib import Path


class DatasetInspector:

    def inspect(
        self,
        directory: Path,
    ):

        files = 0
        size = 0

        for file in directory.rglob("*"):

            if file.is_file():

                files += 1
                size += file.stat().st_size

        return {
            "files": files,
            "bytes": size,
        }
