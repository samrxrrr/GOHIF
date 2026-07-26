from pathlib import Path
import csv
from collections import defaultdict

ROOT = Path("/mnt/g/My Drive/DATASETS")
OUT = ROOT / "_registry" / "dataset_manifest.csv"

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

datasets = defaultdict(list)

for file in ROOT.rglob("*"):

    if not file.is_file():
        continue

    if any(part in IGNORE for part in file.parts):
        continue

    rel = file.relative_to(ROOT)
    parts = rel.parts

    # Dataset = first directory after domain
    if len(parts) >= 2:
        dataset_key = (parts[0], parts[1])
    else:
        dataset_key = (parts[0], file.stem)

    datasets[dataset_key].append(file)

with open(OUT, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "dataset_id",
        "domain",
        "dataset_name",
        "file_count",
        "total_size_bytes",
        "primary_path",
    ])

    for i, ((domain, dataset), files) in enumerate(sorted(datasets.items()), start=1):

        total_size = sum(x.stat().st_size for x in files)

        writer.writerow([
            f"GOHIF_DS_{i:04d}",
            domain,
            dataset,
            len(files),
            total_size,
            str(files[0].parent.relative_to(ROOT)),
        ])

print("=" * 60)
print("GOHIF DATASET MANIFEST CREATED")
print("=" * 60)
print("Logical datasets :", len(datasets))
print("Output :", OUT)
