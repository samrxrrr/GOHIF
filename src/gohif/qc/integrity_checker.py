from pathlib import Path
import csv
import json

ROOT = Path("/mnt/g/My Drive/DATASETS")

CATALOG = ROOT / "_registry" / "dataset_catalog.csv"

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

CSV_REPORT = REPORT_DIR / "dataset_integrity_report.csv"
SUMMARY_REPORT = REPORT_DIR / "dataset_integrity_summary.json"


def dataset_statistics(path: Path):

    if path.is_file():

        return {
            "exists": True,
            "type": "file",
            "files": 1,
            "size": path.stat().st_size,
        }

    if path.is_dir():

        total_files = 0
        total_size = 0

        for f in path.rglob("*"):

            if not f.is_file():
                continue

            total_files += 1

            try:
                total_size += f.stat().st_size
            except Exception:
                pass

        return {
            "exists": True,
            "type": "directory",
            "files": total_files,
            "size": total_size,
        }

    return {
        "exists": False,
        "type": "missing",
        "files": 0,
        "size": 0,
    }


rows = []

summary = {
    "datasets": 0,
    "missing": 0,
    "empty": 0,
    "valid": 0,
}

with open(CATALOG, newline="", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        dataset_path = ROOT / row["dataset_path"]

        stats = dataset_statistics(dataset_path)

        summary["datasets"] += 1

        status = "VALID"

        if not stats["exists"]:

            status = "MISSING"

            summary["missing"] += 1

        elif stats["size"] == 0:

            status = "EMPTY"

            summary["empty"] += 1

        else:

            summary["valid"] += 1

        rows.append({

            "dataset_id": row["dataset_id"],
            "dataset_name": row["dataset_name"],
            "status": status,
            "dataset_type": stats["type"],
            "file_count": stats["files"],
            "size_bytes": stats["size"],

        })

with open(CSV_REPORT, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(

        f,

        fieldnames=[
            "dataset_id",
            "dataset_name",
            "status",
            "dataset_type",
            "file_count",
            "size_bytes",
        ],
    )

    writer.writeheader()

    writer.writerows(rows)

with open(SUMMARY_REPORT, "w", encoding="utf-8") as f:

    json.dump(summary, f, indent=2)

print("=" * 70)
print("GOHIF Dataset Integrity Report")
print("=" * 70)
print(json.dumps(summary, indent=2))
print("=" * 70)
print("CSV :", CSV_REPORT)
print("JSON:", SUMMARY_REPORT)
