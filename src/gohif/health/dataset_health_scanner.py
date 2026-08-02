from pathlib import Path
import csv
from gohif.filetype.file_signature import detect_file_type

ROOT = Path("/mnt/g/My Drive/DATASETS")
CATALOG = ROOT / "_registry" / "dataset_catalog.csv"

REPORT = Path("reports")
REPORT.mkdir(exist_ok=True)

rows = []

with open(CATALOG, newline="", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for ds in reader:

        path = ROOT / ds["dataset_path"]

        if not path.exists():

            rows.append([
                ds["dataset_id"],
                ds["dataset_name"],
                "MISSING",
                "",
                ""
            ])

            continue

        if path.is_dir():

            rows.append([
                ds["dataset_id"],
                ds["dataset_name"],
                "DIRECTORY",
                "",
                ""
            ])

            continue

        detected = detect_file_type(path)

        ext = "".join(path.suffixes).lower()

        status = "OK"

        if ".pdf" in ext and detected != "PDF":
            status = "MISMATCH"

        elif ".zip" in ext and detected != "ZIP":
            status = "MISMATCH"

        elif ".json" in ext and detected != "JSON":
            status = "MISMATCH"

        rows.append([
            ds["dataset_id"],
            ds["dataset_name"],
            status,
            ext,
            detected
        ])

out = REPORT / "dataset_health_report.csv"

with open(out, "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "dataset_id",
        "dataset_name",
        "status",
        "extension",
        "detected_type"
    ])

    writer.writerows(rows)

print("="*70)
print("GOHIF Dataset Health Scan Complete")
print("="*70)
print("Datasets scanned :", len(rows))
print("Report :", out)
print("="*70)
