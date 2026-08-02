from pathlib import Path
import json
import csv
import hashlib
from datetime import datetime

ROOT = Path("/mnt/g/My Drive/DATASETS")
CATALOG = ROOT / "_registry" / "dataset_catalog.csv"

OUTDIR = Path("processed/provenance")
OUTDIR.mkdir(parents=True, exist_ok=True)

rows=[]

def sha256(path):

    h=hashlib.sha256()

    with open(path,"rb") as f:

        while True:

            chunk=f.read(1024*1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()

with open(CATALOG,newline="",encoding="utf-8") as f:

    reader=csv.DictReader(f)

    for ds in reader:

        p=ROOT/ds["dataset_path"]

        if not p.exists():
            continue

        if p.is_dir():

            rows.append({

                "dataset_id":ds["dataset_id"],
                "dataset_name":ds["dataset_name"],
                "path":str(p),
                "type":"directory",
                "size_bytes":0,
                "sha256":"",
                "last_modified":datetime.fromtimestamp(
                    p.stat().st_mtime
                ).isoformat()

            })

            continue

        rows.append({

            "dataset_id":ds["dataset_id"],
            "dataset_name":ds["dataset_name"],
            "path":str(p),
            "type":"file",
            "size_bytes":p.stat().st_size,
            "sha256":sha256(p),
            "last_modified":datetime.fromtimestamp(
                p.stat().st_mtime
            ).isoformat()

        })

outfile=OUTDIR/"dataset_lineage.json"

with open(outfile,"w",encoding="utf-8") as f:

    json.dump(rows,f,indent=2)

print("="*70)
print("GOHIF Provenance Engine Complete")
print("="*70)
print("Datasets :",len(rows))
print("Output   :",outfile)
print("="*70)
