"""
GOHIF REST API Downloader
"""

from pathlib import Path
import requests


class APIDownloader:

    def download(self, url, outfile):

        outfile = Path(outfile)
        outfile.parent.mkdir(parents=True, exist_ok=True)

        print(f"\nDownloading\n{url}\n")

        r = requests.get(url, timeout=120)

        if r.status_code != 200:
            print(f"HTTP {r.status_code}")
            return False

        outfile.write_bytes(r.content)

        return True


if __name__ == "__main__":

    downloader = APIDownloader()

    ok = downloader.download(
        "https://www.ebi.ac.uk/ena/portal/api/search?result=study&limit=1",
        "data/raw/environment/ENA/test.json"
    )

    print("\nSUCCESS" if ok else "\nFAILED")
