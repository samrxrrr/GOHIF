"""
GOHIF Download Manager

Reads the download manifest and dispatches datasets
to the appropriate download backend.

Version: 1.0
"""

from __future__ import annotations

import pandas as pd

try:
    from .http_downloader import download as http_download
    from .ncbi_downloader import NCBIDownloader
    from .api_downloader import APIDownloader
except ImportError:
    from http_downloader import download as http_download
    from ncbi_downloader import NCBIDownloader
    from api_downloader import APIDownloader


MANIFEST = "metadata/downloads/GOHIF_Download_Manifest.csv"


def show_summary(df):

    print("\n==============================")
    print("GOHIF DOWNLOAD MANIFEST")
    print("==============================")

    print(f"Total datasets : {len(df)}")

    print("\nAutomation levels")
    print(df["Automation"].value_counts(dropna=False))

    print("\nDownload methods")
    print(df["Download_Method"].value_counts(dropna=False))

    print("==============================\n")


def main():

    df = pd.read_csv(MANIFEST).fillna("")

    show_summary(df)

    ncbi = NCBIDownloader()
    api = APIDownloader()

    print("Dispatcher initialized.")

    print("\nConfigured datasets:\n")

    cols = [
        "GOHIF_ID",
        "Dataset_Name",
        "Download_Method",
        "Automation",
    ]

    print(df[df["Automation"] == "Full"][cols].to_string(index=False))

    print("\nNo downloads executed.")
    print("Framework ready.")


if __name__ == "__main__":
    main()
