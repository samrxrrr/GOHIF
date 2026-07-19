"""
GOHIF SRA Toolkit Downloader

Author: GOHIF
"""

from pathlib import Path
import subprocess

from base import BaseDownloader


class SRADownloader(BaseDownloader):
    """
    Download SRA datasets using NCBI SRA Toolkit.
    """

    def download(
        self,
        accession,
        output_dir,
        threads=8,
        keep_sra=True,
    ):

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        print("\n======================================")
        print("GOHIF SRA DOWNLOAD")
        print("======================================")
        print(f"Accession : {accession}")
        print()

        prefetch_cmd = [
            "prefetch",
            accession,
            "--output-directory",
            str(output_dir),
        ]

        print("Executing:")
        print(" ".join(prefetch_cmd))
        print()

        result = subprocess.run(prefetch_cmd)

        if result.returncode != 0:
            return False

        sra_file = (
            output_dir
            / accession
            / f"{accession}.sra"
        )

        fastq_dir = output_dir / "FASTQ"
        fastq_dir.mkdir(exist_ok=True)

        fasterq_cmd = [
            "fasterq-dump",
            str(sra_file),
            "-O",
            str(fastq_dir),
            "-e",
            str(threads),
        ]

        print()
        print("Executing:")
        print(" ".join(fasterq_cmd))
        print()

        result = subprocess.run(fasterq_cmd)

        if result.returncode != 0:
            return False

        if not keep_sra:
            sra_file.unlink(missing_ok=True)

        return True


if __name__ == "__main__":

    downloader = SRADownloader()

    ok = downloader.download(
        accession="SRR390728",
        output_dir="data/raw/genomics/SRA",
    )

    print("\nSUCCESS" if ok else "\nFAILED")
