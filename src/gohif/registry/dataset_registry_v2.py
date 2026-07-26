from pathlib import Path
from datetime import datetime
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

OUT.parent.mkdir(parents=True, exist_ok=True)

count = 0

with open(OUT, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "domain",
        "relative_path",
        "filename",
        "extension",
        "size_bytes",
        "modified",
        "compressed"
    ])

    for file in ROOT.rglob("*"):

        if not file.is_file():
            continue

        if any(part in IGNORE for part in file.parts):
            continue

        rel = file.relative_to(ROOT)

        writer.writerow([
            rel.parts[0],
            str(rel),
            file.name,
            file.suffix.lower(),
            file.stat().st_size,
            datetime.fromtimestamp(
                file.stat().st_mtime
            ).isoformat(),
            file.suffix.lower() in {
                ".zip",
                ".gz",
                ".bz2",
                ".tar",
                ".tgz"
            }
        ])

        count += 1

        if count % 100 == 0:
            print(f"Indexed {count} files...")

print("\nDone")
print("Datasets:", count)
print("Saved to:", OUT)
