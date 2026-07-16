from pathlib import Path
import json
import csv

ROOT = Path(__file__).resolve().parents[2]

REGISTRY = ROOT / "data" / "registry" / "datasets"

OUTDIR = ROOT / "docs" / "MDI"

OUTDIR.mkdir(parents=True, exist_ok=True)

csv_file = OUTDIR / "Master_Dataset_Inventory.csv"
md_file = OUTDIR / "Master_Dataset_Inventory.md"

datasets = []

for f in sorted(REGISTRY.glob("*.json")):
    with open(f, encoding="utf-8") as fp:
        datasets.append(json.load(fp))

datasets.sort(key=lambda x: x["id"])

###############################################################################
# CSV
###############################################################################

fields = [
    "id",
    "name",
    "domain",
    "organization",
    "tier",
    "evidence_class",
    "status"
]

with open(csv_file, "w", newline="", encoding="utf-8") as fp:
    writer = csv.DictWriter(fp, fieldnames=fields)
    writer.writeheader()

    for ds in datasets:
        writer.writerow({k: ds.get(k, "") for k in fields})

###############################################################################
# MARKDOWN
###############################################################################

with open(md_file, "w", encoding="utf-8") as fp:

    fp.write("# GOHIF Master Dataset Inventory\n\n")
    fp.write("Status: Auto-generated\n\n")
    fp.write(f"Datasets Registered: **{len(datasets)}**\n\n")

    current = None

    for ds in datasets:

        if ds["domain"] != current:
            current = ds["domain"]
            fp.write(f"\n---\n\n## {current}\n\n")

        fp.write(f"### {ds['id']} — {ds['name']}\n")
        fp.write(f"- Organization: {ds['organization']}\n")
        fp.write(f"- Tier: {ds['tier']}\n")
        fp.write(f"- Evidence Class: {ds['evidence_class']}\n")
        fp.write(f"- Status: {ds['status']}\n\n")

print(f"[OK] Generated CSV : {csv_file}")
print(f"[OK] Generated MD  : {md_file}")
print(f"[OK] Total datasets: {len(datasets)}")
