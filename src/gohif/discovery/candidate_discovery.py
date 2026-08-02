from pathlib import Path
import json
import csv
from collections import Counter

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")
OUTPUT = Path("processed/discovery")

OUTPUT.mkdir(parents=True, exist_ok=True)

entity_counter = Counter()
entity_domains = {}

FIELDS = [
    "genes",
    "species",
    "pathogens",
    "diseases"
]

for artifact_file in sorted(ARTIFACTS.glob("*.json")):

    with open(artifact_file, encoding="utf-8") as f:
        art = json.load(f)

    domain = art["metadata"].get("domain","")

    for field in FIELDS:

        for entity in art["entities"].get(field,[]):

            key = (field, entity)

            entity_counter[key] += 1

            entity_domains.setdefault(key,set()).add(domain)

rows=[]

for (etype, entity), freq in entity_counter.items():

    domains = sorted(entity_domains[(etype,entity)])

    score = freq * len(domains)

    rows.append([

        etype,

        entity,

        freq,

        len(domains),

        score,

        ";".join(domains)

    ])

rows.sort(key=lambda x:x[4], reverse=True)

with open(OUTPUT/"research_candidates.csv","w",newline="",encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "entity_type",
        "entity",
        "frequency",
        "domains",
        "priority_score",
        "domain_list"
    ])

    writer.writerows(rows)

summary = {

    "candidate_entities":len(rows),

    "highest_priority":rows[0] if rows else None

}

with open(OUTPUT/"summary.json","w",encoding="utf-8") as f:

    json.dump(summary,f,indent=2)

print("="*70)
print("GOHIF Candidate Discovery Complete")
print("="*70)
print(json.dumps(summary,indent=2))
print("="*70)
