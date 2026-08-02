from pathlib import Path
import csv
import json
from collections import defaultdict

INPUT = Path("processed/discovery/research_candidates.csv")
OUTPUT = Path("processed/ranking")

OUTPUT.mkdir(parents=True, exist_ok=True)

weights = {
    "genes":5,
    "pathogens":4,
    "diseases":3,
    "species":2,
}

rows=[]

with open(INPUT,encoding="utf-8") as f:

    reader=csv.DictReader(f)

    for row in reader:

        entity_type=row["entity_type"]

        priority=int(row["priority_score"])

        frequency=int(row["frequency"])

        domains=int(row["domains"])

        score=priority*weights.get(entity_type,1)

        rows.append({

            "entity":row["entity"],

            "entity_type":entity_type,

            "frequency":frequency,

            "domains":domains,

            "priority_score":priority,

            "impact_score":score,

            "domain_list":row["domain_list"]

        })

rows.sort(key=lambda x:x["impact_score"],reverse=True)

with open(OUTPUT/"one_health_hotspots.csv","w",newline="",encoding="utf-8") as f:

    writer=csv.DictWriter(f,fieldnames=[
        "entity",
        "entity_type",
        "frequency",
        "domains",
        "priority_score",
        "impact_score",
        "domain_list"
    ])

    writer.writeheader()

    writer.writerows(rows)

summary={

    "ranked_entities":len(rows),

    "top10":[
        r["entity"] for r in rows[:10]
    ]

}

with open(OUTPUT/"summary.json","w",encoding="utf-8") as f:

    json.dump(summary,f,indent=2)

print("="*70)
print("GOHIF One Health Hotspot Ranking Complete")
print("="*70)
print(json.dumps(summary,indent=2))
print("="*70)
