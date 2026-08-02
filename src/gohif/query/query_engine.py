from pathlib import Path
import json
from difflib import SequenceMatcher

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")

datasets=[]

for file in sorted(ARTIFACTS.glob("*.json")):
    with open(file,encoding="utf-8") as f:
        datasets.append(json.load(f))

print("="*70)
print("GOHIF Semantic Query Engine v2")
print("Type 'exit' to quit")
print("="*70)

while True:

    query=input("\nGOHIF> ").strip().lower()

    if query in ("exit","quit"):
        break

    hits=[]

    for ds in datasets:

        searchable=[]

        meta=ds["metadata"]
        ent=ds["entities"]

        searchable.extend([
            meta.get("dataset_name",""),
            meta.get("title",""),
            meta.get("provider",""),
            meta.get("domain","")
        ])

        for values in ent.values():
            searchable.extend(values)

        best=0

        for item in searchable:

            text=str(item).lower()

            if query in text:
                score=100
            else:
                score=int(
                    SequenceMatcher(
                        None,
                        query,
                        text
                    ).ratio()*100
                )

            if score>best:
                best=score

        if best>=60:
            hits.append((best,ds))

    hits.sort(reverse=True,key=lambda x:x[0])

    print("\nMatches:",len(hits))

    for score,ds in hits[:15]:

        print("-"*65)
        print("Score    :",score)
        print("Dataset  :",ds["dataset_id"])
        print("Name     :",ds["metadata"].get("dataset_name"))
        print("Domain   :",ds["metadata"].get("domain"))
        print("Provider :",ds["metadata"].get("provider"))

print("\nSession finished.")
