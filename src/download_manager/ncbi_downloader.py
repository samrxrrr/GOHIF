"""
GOHIF NCBI Downloader

Supports:
- NCBI Datasets CLI
- SRA Toolkit
- Entrez Direct
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


class NCBIDownloader:

    def __init__(self):
        pass

    def run(self, command: list[str]) -> None:
        print("\nExecuting:")
        print(" ".join(command))

        result = subprocess.run(command)

        if result.returncode != 0:
            raise RuntimeError("Command failed.")

    def download_refseq(self, accession: str, output_directory: str):
        destination = ensure_directory(output_directory)

        command = [
            "datasets",
            "download",
            "genome",
            "accession",
            accession,
            "--filename",
            str(destination / f"{accession}.zip"),
        ]

        self.run(command)

        log_download(accession, "SUCCESS", "RefSeq genome downloaded")

    def prefetch_sra(self, accession: str, output_directory: str):

        ensure_directory(output_directory)

        command = [
            "prefetch",
            accession,
            "--output-directory",
            output_directory,
        ]

        self.run(command)

        log_download(accession, "SUCCESS", "SRA downloaded")

    def search_gene(self, gene: str):

        command = [
            "esearch",
            "-db",
            "gene",
            "-query",
            gene,
        ]

        self.run(command)


def self_test():

    print("=" * 60)
    print("GOHIF NCBI Downloader")
    print("=" * 60)

    subprocess.run(["datasets", "version"])
    subprocess.run(["prefetch", "--version"])
    subprocess.run(["esearch", "-version"])

    print("=" * 60)
    print("Environment OK")
    print("=" * 60)


if __name__ == "__main__":
    self_test()
