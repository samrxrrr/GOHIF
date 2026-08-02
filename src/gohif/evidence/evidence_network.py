from pathlib import Path
import json
import csv
from collections import defaultdict

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")
OUTPUT = Path("processed/evidence")

OUTPUT.mkdir(parents=True, exist_ok=True)

entity_index = defaultdict(list)

ENTITY_FIELDS = [
    "genes",
    "species",
    "diseases",
    "pathogens",
    "countries",
]

for file in sorted(ARTIFACTS.glob("*.json")):

    with open(file, encoding="utf-8") as f:
        art = json.load(f)

    dataset = art["dataset_id"]
    domain = art["metadata"].get("domain", "")

    for field in ENTITY_FIELDS:

        for entity in art["entities"].get(field, []):

            entity_index[(field, entity)].append({

                "dataset": dataset,
                "domain": domain

            })

rows = []

for (etype, entity), refs in sorted(entity_index.items()):

    if len(refs) < 2:
        continue

    domains = sorted({r["domain"] for r in refs})

    datasets = sorted({r["dataset"] for r in refs})

    rows.append([

        etype,

        entity,

        len(datasets),

        len(domains),

        ";".join(domains),

        ";".join(datasets)

    ])

with open(OUTPUT/"entity_evidence_network.csv","w",newline="",encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([

        "entity_type",
        "entity",
        "dataset_count",
        "domain_count",
        "domains",
        "datasets"

    ])

    writer.writerows(rows)

summary = {

    "shared_entities": len(rows),

    "cross_domain_entities": sum(
        1 for r in rows if r[3] > 1
    )

}

with open(OUTPUT/"summary.json","w",encoding="utf-8") as f:

    json.dump(summary,f,indent=2)

print("="*70)
print("GOHIF Evidence Network Built")
print("="*70)
print(json.dumps(summary,indent=2))
print("="*70)
