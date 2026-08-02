from pathlib import Path
import csv

ROOT = Path("/mnt/g/My Drive/DATASETS")
OUT = ROOT / "_registry" / "dataset_catalog.csv"

IGNORE_NAMES = {
    "desktop.ini",
    ".ds_store",
}

IGNORE_SUFFIXES = {
    ".tmp",
    ".lock",
}

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".ipynb_checkpoints",
}


def is_ignored(path: Path):
    if path.name.lower() in IGNORE_NAMES:
        return True

    if path.suffix.lower() in IGNORE_SUFFIXES:
        return True

    for part in path.parts:
        if part in IGNORE_DIRS:
            return True

    return False


records = []
dataset_id = 1

for domain in sorted(ROOT.iterdir()):

    if not domain.is_dir():
        continue

    if domain.name.startswith("_"):
        continue

    #
    # standalone files
    #
    for f in sorted(domain.iterdir()):

        if is_ignored(f):
            continue

        if f.is_file():

            records.append({

                "dataset_id": f"GOHIF_DS_{dataset_id:04d}",
                "domain": domain.name,
                "dataset_name": f.name,
                "dataset_path": str(f.relative_to(ROOT)),
                "dataset_type": "single_file"

            })

            dataset_id += 1

    #
    # subdirectories become independent datasets
    #
    for d in sorted(domain.iterdir()):

        if is_ignored(d):
            continue

        if d.is_dir():

            records.append({

                "dataset_id": f"GOHIF_DS_{dataset_id:04d}",
                "domain": domain.name,
                "dataset_name": d.name,
                "dataset_path": str(d.relative_to(ROOT)),
                "dataset_type": "directory"

            })

            dataset_id += 1


with open(OUT, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(

        f,

        fieldnames=[
            "dataset_id",
            "domain",
            "dataset_name",
            "dataset_path",
            "dataset_type",
        ],
    )

    writer.writeheader()

    writer.writerows(records)

print(f"Datasets discovered: {len(records)}")
print(OUT)
