from __future__ import annotations

import gzip
import shutil
import tarfile
import zipfile
from pathlib import Path


class ArchiveExtractor:

    def extract(
        self,
        archive: Path,
        destination: Path,
    ):

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        suffixes = "".join(archive.suffixes)

        if suffixes.endswith(".zip"):

            with zipfile.ZipFile(archive) as zf:
                zf.extractall(destination)

            return

        if suffixes.endswith(".tar.gz"):

            with tarfile.open(archive,"r:gz") as tf:
                tf.extractall(destination)

            return

        if suffixes.endswith(".tar"):

            with tarfile.open(archive,"r") as tf:
                tf.extractall(destination)

            return

        if suffixes.endswith(".gz"):

            output = destination / archive.stem

            with gzip.open(archive,"rb") as src:
                with open(output,"wb") as dst:
                    shutil.copyfileobj(src,dst)

            return

        raise RuntimeError(
            f"Unsupported archive: {archive}"
        )
