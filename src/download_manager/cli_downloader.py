"""
GOHIF Generic CLI Downloader

Author: GOHIF
"""

from pathlib import Path
import subprocess

from base import BaseDownloader


class CLIDownloader(BaseDownloader):
    """
    Execute arbitrary command-line downloads defined in the manifest.
    """

    def download(self, command, working_directory="."):

        working_directory = Path(working_directory)
        working_directory.mkdir(parents=True, exist_ok=True)

        print("\n======================================")
        print("GOHIF CLI DOWNLOAD")
        print("======================================")
        print(command)
        print()

        result = subprocess.run(
            command,
            shell=True,
            cwd=working_directory,
        )

        return result.returncode == 0


if __name__ == "__main__":

    downloader = CLIDownloader()

    ok = downloader.download(
        "amrfinder --version"
    )

    print("\nSUCCESS" if ok else "\nFAILED")
