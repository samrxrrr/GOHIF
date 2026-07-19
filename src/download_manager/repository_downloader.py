"""
GOHIF Repository Downloader
"""

from pathlib import Path
import subprocess


class RepositoryDownloader:

    def download(self, repo_url, destination):

        destination = Path(destination)

        destination.parent.mkdir(parents=True, exist_ok=True)

        if destination.exists():

            print("\nRepository already exists.")
            print("Updating repository...\n")

            cmd = [
                "git",
                "-C",
                str(destination),
                "pull",
                "--ff-only"
            ]

        else:

            print("\nCloning repository...\n")

            cmd = [
                "git",
                "clone",
                repo_url,
                str(destination)
            ]

        print("Executing:")
        print(" ".join(cmd))

        result = subprocess.run(cmd)

        return result.returncode == 0


if __name__ == "__main__":

    downloader = RepositoryDownloader()

    ok = downloader.download(
        "https://bitbucket.org/genomicepidemiology/resfinder_db.git",
        "data/raw/genomics/ResFinder"
    )

    print("\nSUCCESS" if ok else "\nFAILED")
