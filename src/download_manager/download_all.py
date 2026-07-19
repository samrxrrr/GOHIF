"""
GOHIF Download Engine v3
"""

from pathlib import Path
import hashlib

from manifest import ManifestManager
from dispatcher import DownloadDispatcher
from http_downloader import download as http_download

MANIFEST = "metadata/downloads/GOHIF_Download_Manifest.csv"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def filesize(path):
    return Path(path).stat().st_size / (1024 * 1024)


def output_file(row):

    dataset = row["Dataset_Name"]

    mapping = {
        "CARD": "data/raw/genomics/CARD/card_data.tar.bz2",
        "MEGARes": "data/raw/genomics/MEGARes/megares_v3.00.zip",
        "BacMet": "data/raw/genomics/BacMet/BacMet2_EXP_database.fasta",
        "PLSDB": "data/raw/genomics/PLSDB/plsdb.fna.bz2",
    }

    return mapping.get(dataset)


def main():

    manifest = ManifestManager(MANIFEST)
    dispatcher = DownloadDispatcher()

    print("=" * 70)
    print("GOHIF DOWNLOAD ENGINE")
    print("=" * 70)

    for idx, row in manifest.datasets():

        backend = dispatcher.dispatch(row)

        if backend != "HTTP":
            continue

        outfile = output_file(row)

        if outfile is None:
            continue

        print(f"\nDownloading {row['Dataset_Name']}...\n")

        ok = http_download(
            row["Download_URL"],
            outfile
        )

        if ok:

            manifest.update(
                idx,
                status="Success",
                local_file=outfile,
                sha256=sha256(outfile),
                size_mb=filesize(outfile),
                error=""
            )

            print("SUCCESS\n")

        else:

            manifest.update(
                idx,
                status="Failed",
                error="Download failed"
            )

            print("FAILED\n")


if __name__ == "__main__":
    main()
