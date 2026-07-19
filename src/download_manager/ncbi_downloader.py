"""
GOHIF NCBI Datasets Downloader
"""

from pathlib import Path
import subprocess


class NCBIDownloader:

    def download(self, accession, output_dir):

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        zipfile = output_dir / f"{accession}.zip"

        cmd = [
            "datasets",
            "download",
            "genome",
            "accession",
            accession,
            "--filename",
            str(zipfile)
        ]

        print("\nExecuting:")
        print(" ".join(cmd))
        print()

        result = subprocess.run(cmd)

        return result.returncode == 0


if __name__ == "__main__":

    downloader = NCBIDownloader()

    ok = downloader.download(
        "GCF_000005845.2",
        "data/raw/genomics/RefSeq"
    )

    print("\nSUCCESS" if ok else "\nFAILED")
