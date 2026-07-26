from pathlib import Path
import zipfile
import gzip
import tarfile
import bz2
import shutil
import csv

ROOT = Path("/mnt/g/My Drive/DATASETS")
OUT_ROOT = ROOT / "_extracted"
LOG_DIR = ROOT / "_logs"

OUT_ROOT.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "extraction_log.csv"

ARCHIVES = {
    ".zip",
    ".gz",
    ".bz2",
    ".tar",
    ".tgz",
}

rows = []


def extract_zip(src, dest):
    with zipfile.ZipFile(src) as z:
        z.extractall(dest)


def extract_gz(src, dest):
    outfile = dest / src.stem
    with gzip.open(src, "rb") as fin:
        with open(outfile, "wb") as fout:
            shutil.copyfileobj(fin, fout)


def extract_bz2(src, dest):
    outfile = dest / src.stem
    with bz2.open(src, "rb") as fin:
        with open(outfile, "wb") as fout:
            shutil.copyfileobj(fin, fout)


def extract_tar(src, dest):
    with tarfile.open(src) as t:
        t.extractall(dest)


for file in ROOT.rglob("*"):

    if not file.is_file():
        continue

    if "_extracted" in file.parts:
        continue

    if "_logs" in file.parts:
        continue

    suffix = file.suffix.lower()

    if suffix not in ARCHIVES:
        continue

    if file.stat().st_size == 0:
        rows.append([str(file), "EMPTY", "Skipped"])
        continue

    domain = file.relative_to(ROOT).parts[0]

    destination = OUT_ROOT / domain / file.stem

    if destination.exists():
        rows.append([str(file), "EXISTS", "Skipped"])
        continue

    destination.mkdir(parents=True, exist_ok=True)

    try:

        if suffix == ".zip":
            extract_zip(file, destination)

        elif suffix == ".gz":
            extract_gz(file, destination)

        elif suffix == ".bz2":
            extract_bz2(file, destination)

        elif suffix in {".tar", ".tgz"}:
            extract_tar(file, destination)

        rows.append([str(file), "SUCCESS", str(destination)])

        print("Extracted:", file.name)

    except Exception as e:

        rows.append([str(file), "FAILED", str(e)])

        print("Failed:", file.name)


with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow(["Archive", "Status", "Output"])

    writer.writerows(rows)

print("\nExtraction complete.")
print("Log:", LOG_FILE)
