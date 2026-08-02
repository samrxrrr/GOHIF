from pathlib import Path
import csv
import hashlib
import json

ROOT = Path("/mnt/g/My Drive/DATASETS")

CATALOG = ROOT / "_registry" / "dataset_catalog.csv"

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

DUP_REPORT = REPORT_DIR / "duplicate_hashes.csv"
SUMMARY = REPORT_DIR / "duplicate_summary.json"


def sha256(path, chunk_size=1024 * 1024):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


hash_index = {}

with open(CATALOG, newline="", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        dataset_path = ROOT / row["dataset_path"]

        files = []

        if dataset_path.is_file():

            files.append(dataset_path)

        elif dataset_path.is_dir():

            files.extend(
                p for p in dataset_path.rglob("*")
                if p.is_file()
            )

        for file in files:

            try:

                digest = sha256(file)

            except Exception:

                continue

            hash_index.setdefault(digest, []).append(file)


duplicates = []

for digest, files in hash_index.items():

    if len(files) < 2:
        continue

    for f in files:

        duplicates.append({

            "sha256": digest,

            "file": str(f.relative_to(ROOT))

        })


with open(DUP_REPORT, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(

        f,

        fieldnames=[
            "sha256",
            "file",
        ],

    )

    writer.writeheader()

    writer.writerows(duplicates)


summary = {

    "unique_hashes": len(hash_index),

    "duplicate_groups":
        len([h for h in hash_index.values() if len(h) > 1]),

    "duplicate_files":
        len(duplicates)

}

with open(SUMMARY, "w", encoding="utf-8") as f:

    json.dump(summary, f, indent=2)

print("=" * 70)
print(json.dumps(summary, indent=2))
print("=" * 70)
print("Report:", DUP_REPORT)
