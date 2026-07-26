from pathlib import Path
from datetime import datetime
import hashlib
import zipfile
import tarfile
import gzip
import bz2
import csv

ROOT = Path("/mnt/g/My Drive/DATASETS")
OUT = ROOT / "_registry" / "master_dataset_registry.csv"

IGNORE = {
    "_registry",
    "_metadata",
    "_logs",
    "_cache",
    "_processed",
    "_harmonized",
    "_analysis",
    "_reports",
}

ARCHIVE_SUFFIXES = {
    ".zip",
    ".gz",
    ".bz2",
    ".tar",
    ".tgz",
}

rows = []


def sha256(path, blocksize=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            data = f.read(blocksize)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def archive_summary(path):
    try:

        if path.suffix.lower() == ".zip":
            with zipfile.ZipFile(path) as z:
                return len(z.namelist())

        elif path.suffix.lower() in {".tar", ".tgz"}:
            with tarfile.open(path) as t:
                return len(t.getmembers())

        elif path.suffix.lower() == ".gz":
            return 1

        elif path.suffix.lower() == ".bz2":
            return 1

    except Exception:
        return -1

    return 0


for file in ROOT.rglob("*"):

    if not file.is_file():
        continue

    if any(part in IGNORE for part in file.parts):
        continue

    rel = file.relative_to(ROOT)

    domain = rel.parts[0]

    size = file.stat().st_size

    modified = datetime.fromtimestamp(
        file.stat().st_mtime
    ).isoformat()

    suffix = file.suffix.lower()

    compressed = suffix in ARCHIVE_SUFFIXES

    archive_files = archive_summary(file) if compressed else ""

    try:
        checksum = sha256(file)
    except Exception:
        checksum = ""

    rows.append([
        domain,
        str(rel),
        file.name,
        suffix,
        size,
        modified,
        compressed,
        archive_files,
        checksum,
    ])

OUT.parent.mkdir(exist_ok=True)

with open(OUT, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "domain",
        "relative_path",
        "filename",
        "extension",
        "size_bytes",
        "modified",
        "compressed",
        "archive_entries",
        "sha256",
    ])

    writer.writerows(rows)

print("=" * 60)
print("GOHIF MASTER DATASET REGISTRY CREATED")
print("=" * 60)
print("Datasets:", len(rows))
print("Output:", OUT)
