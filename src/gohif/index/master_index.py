from pathlib import Path
import json
import csv

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")

OUTPUT = Path("processed/index")
OUTPUT.mkdir(parents=True, exist_ok=True)

rows=[]

for file in sorted(ARTIFACTS.glob("*.json")):

    with open(file,encoding="utf-8") as f:
        art=json.load(f)

    meta=art["metadata"]
    ent=art["entities"]

    rows.append({

        "dataset_id":art["dataset_id"],

        "dataset_name":meta.get("dataset_name",""),

        "domain":meta.get("domain",""),

        "provider":meta.get("provider",""),

        "type":meta.get("dataset_type",""),

        "path":meta.get("dataset_path",""),

        "genes":len(ent.get("genes",[])),

        "proteins":len(ent.get("proteins",[])),

        "species":len(ent.get("species",[])),

        "diseases":len(ent.get("diseases",[])),

        "pathogens":len(ent.get("pathogens",[])),

        "countries":len(ent.get("countries",[])),

        "keywords":len(meta.get("keywords",[]))

    })

outfile=OUTPUT/"master_index.csv"

with open(outfile,"w",newline="",encoding="utf-8") as f:

    writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()))

    writer.writeheader()

    writer.writerows(rows)

print("="*70)
print("GOHIF Master Data Lake Index Built")
print("="*70)
print("Datasets :",len(rows))
print("Output   :",outfile)
print("="*70)
