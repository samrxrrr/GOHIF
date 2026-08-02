from pathlib import Path
import json
import csv
from itertools import combinations
from collections import defaultdict

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")
OUTPUT = Path("processed/associations")

OUTPUT.mkdir(parents=True, exist_ok=True)

datasets = []

for file in sorted(ARTIFACTS.glob("*.json")):

    with open(file, encoding="utf-8") as f:
        art = json.load(f)

    datasets.append({

        "id": art["dataset_id"],

        "domain": art["metadata"].get("domain",""),

        "entities": set(
            art["entities"].get("genes",[]) +
            art["entities"].get("species",[]) +
            art["entities"].get("diseases",[]) +
            art["entities"].get("pathogens",[]) +
            art["entities"].get("countries",[])
        )

    })

rows=[]

cross=defaultdict(int)

for A,B in combinations(datasets,2):

    if A["domain"]==B["domain"]:
        continue

    shared=A["entities"] & B["entities"]

    if not shared:
        continue

    rows.append([

        A["id"],
        A["domain"],
        B["id"],
        B["domain"],
        len(shared),
        "; ".join(sorted(shared))

    ])

    pair=" <-> ".join(sorted([A["domain"],B["domain"]]))

    cross[pair]+=1

with open(OUTPUT/"cross_domain_links.csv","w",newline="",encoding="utf-8") as f:

    writer=csv.writer(f)

    writer.writerow([
        "dataset_a",
        "domain_a",
        "dataset_b",
        "domain_b",
        "shared_entities",
        "entities"
    ])

    writer.writerows(rows)

summary={

    "cross_domain_relationships":len(rows),

    "domain_pairs":dict(cross)

}

with open(OUTPUT/"summary.json","w",encoding="utf-8") as f:

    json.dump(summary,f,indent=2)

print("="*70)
print("Cross-Domain Association Engine Complete")
print("="*70)
print(json.dumps(summary,indent=2))
print("="*70)
