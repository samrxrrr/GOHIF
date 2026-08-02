from pathlib import Path
import csv

ROOT = Path("/mnt/g/My Drive/DATASETS")
CATALOG = ROOT / "_registry" / "dataset_catalog.csv"

REPORT = Path("reports")
REPORT.mkdir(exist_ok=True)

rows=[]

with open(CATALOG,newline="",encoding="utf-8") as f:

    reader=csv.DictReader(f)

    for ds in reader:

        p=ROOT/ds["dataset_path"]

        if not p.exists():
            continue

        if p.is_dir():
            continue

        try:

            with open(p,"rb") as fp:
                header=fp.read(2048)

            text=header.decode("utf-8","ignore").lower()

        except Exception:
            text=""

        problem=""

        recommendation=""

        if "<html" in text or "<!doctype" in text:

            problem="HTML page saved instead of dataset"

            recommendation="Re-download from original source"

        elif "404" in text:

            problem="404 page"

            recommendation="Broken download"

        elif "access denied" in text:

            problem="Access denied"

            recommendation="Authenticate before downloading"

        elif "forbidden" in text:

            problem="Forbidden"

            recommendation="Check permissions"

        elif len(header)<100:

            problem="Very small file"

            recommendation="Verify download"

        else:

            continue

        rows.append([

            ds["dataset_id"],

            ds["dataset_name"],

            p.name,

            problem,

            recommendation

        ])

out=REPORT/"dataset_repair_report.csv"

with open(out,"w",newline="",encoding="utf-8") as f:

    writer=csv.writer(f)

    writer.writerow([

        "dataset_id",

        "dataset_name",

        "filename",

        "problem",

        "recommendation"

    ])

    writer.writerows(rows)

print("="*70)
print("GOHIF Dataset Repair Scan Complete")
print("="*70)
print("Datasets requiring attention:",len(rows))
print("Output:",out)
print("="*70)
