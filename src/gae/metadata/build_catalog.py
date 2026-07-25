from pathlib import Path
import json
import csv

PROFILE_DIR = Path.home()/"GoogleDrive"/"GOHIF_DATA"/"01_METADATA"/"Profiles"
OUT = Path("catalog")/"MASTER_METADATA_CATALOG.csv"

rows = []

for profile in sorted(PROFILE_DIR.glob("*.json")):

    with open(profile) as f:
        p = json.load(f)

    rows.append({
        "Name": p.get("name",""),
        "Type": p.get("type",""),
        "Extension": p.get("extension",""),
        "Size": p.get("size",""),
        "SHA256": p.get("sha256",""),
        "Columns": p.get("column_count",""),
        "SampleRows": p.get("sample_rows",""),
        "Sequences": p.get("sequence_count",""),
        "Keys": len(p.get("keys",[])),
        "File": p.get("file","")
    })

OUT.parent.mkdir(exist_ok=True)

with open(OUT,"w",newline="") as f:

    writer=csv.DictWriter(
        f,
        fieldnames=[
            "Name",
            "Type",
            "Extension",
            "Size",
            "SHA256",
            "Columns",
            "SampleRows",
            "Sequences",
            "Keys",
            "File"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)

print()
print("===================================")
print("MASTER METADATA CATALOG GENERATED")
print("===================================")
print("Datasets :",len(rows))
print("Output   :",OUT)
