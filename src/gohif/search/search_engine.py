from pathlib import Path
import json
from collections import defaultdict

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")
OUTPUT = Path("processed/search")

OUTPUT.mkdir(parents=True, exist_ok=True)

index = defaultdict(list)

FIELDS = [
    "provider",
    "domain",
    "dataset_name",
    "title",
    "keywords",
    "countries",
    "species",
    "genes",
    "proteins",
    "diseases",
    "pathogens",
]

for artifact_file in sorted(ARTIFACTS.glob("*.json")):

    with open(artifact_file, encoding="utf-8") as f:
        art = json.load(f)

    dataset = art["dataset_id"]

    metadata = art.get("metadata", {})
    entities = art.get("entities", {})

    values = {

        "provider":[metadata.get("provider","")],

        "domain":[metadata.get("domain","")],

        "dataset_name":[metadata.get("dataset_name","")],

        "title":[metadata.get("title","")],

        "keywords":metadata.get("keywords",[]),

        "countries":entities.get("countries",[]),

        "species":entities.get("species",[]),

        "genes":entities.get("genes",[]),

        "proteins":entities.get("proteins",[]),

        "diseases":entities.get("diseases",[]),

        "pathogens":entities.get("pathogens",[]),

    }

    for field in FIELDS:

        for value in values[field]:

            if not value:
                continue

            key = value.strip().lower()

            index[key].append({
                "dataset":dataset,
                "field":field
            })

with open(OUTPUT/"semantic_index.json","w",encoding="utf-8") as f:
    json.dump(index,f,indent=2)

print("="*70)
print("Semantic Search Index Built")
print("="*70)
print("Indexed Terms :",len(index))
print("="*70)
