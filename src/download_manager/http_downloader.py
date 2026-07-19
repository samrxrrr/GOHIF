"""
GOHIF HTTP Downloader
"""

from pathlib import Path
import subprocess


def download(url, output_file):

    output_file = Path(output_file)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "wget",
        "-c",
        url,
        "-O",
        str(output_file)
    ]

    print("Executing:")
    print(" ".join(cmd))

    result = subprocess.run(cmd)

    return result.returncode == 0


def self_test():

    print("="*60)
    print("GOHIF HTTP Downloader")
    print("="*60)

    subprocess.run(["wget","--version"])


if __name__ == "__main__":
    self_test()
