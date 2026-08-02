from pathlib import Path
import json
import itertools
import csv

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")
OUTPUT = Path("processed/similarity")

OUTPUT.mkdir(parents=True, exist_ok=True)

datasets = {}

for file in sorted(ARTIFACTS.glob("*.json")):

    with open(file, encoding="utf-8") as f:
        art = json.load(f)

    entities = set()

    for field in [
        "genes",
        "species",
        "diseases",
        "pathogens",
        "countries",
    ]:
        entities.update(art["entities"].get(field, []))

    datasets[art["dataset_id"]] = entities

rows = []

for a, b in itertools.combinations(sorted(datasets), 2):

    A = datasets[a]
    B = datasets[b]

    if not A and not B:
        continue

    union = A | B

    if not union:
        continue

    score = len(A & B) / len(union)

    if score > 0:

        rows.append([

            a,

            b,

            round(score,4),

            len(A & B)

        ])

rows.sort(key=lambda x: x[2], reverse=True)

with open(OUTPUT/"dataset_similarity.csv","w",newline="",encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([

        "dataset_a",

        "dataset_b",

        "jaccard_similarity",

        "shared_entities"

    ])

    writer.writerows(rows)

summary = {

    "datasets":len(datasets),

    "relationships":len(rows),

    "max_similarity":rows[0][2] if rows else 0

}

with open(OUTPUT/"summary.json","w",encoding="utf-8") as f:

    json.dump(summary,f,indent=2)

print("="*70)
print("Dataset Similarity Network Built")
print("="*70)
print(summary)
print("="*70)
