from pathlib import Path
import json

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")

datasets=[]

for file in sorted(ARTIFACTS.glob("*.json")):

    with open(file,encoding="utf-8") as f:
        datasets.append(json.load(f))

print("="*70)
print("GOHIF Interactive Query Engine")
print("Type 'exit' to quit")
print("="*70)

while True:

    query=input("\nGOHIF> ").strip()

    if query.lower() in ("exit","quit"):
        break

    query=query.lower()

    hits=[]

    for ds in datasets:

        score=0

        meta=ds["metadata"]
        ent=ds["entities"]

        searchable=[]

        searchable.append(meta.get("dataset_name",""))
        searchable.append(meta.get("title",""))
        searchable.append(meta.get("provider",""))
        searchable.append(meta.get("domain",""))

        for field in ent.values():
            searchable.extend(field)

        text=" ".join(map(str,searchable)).lower()

        if query in text:
            score=text.count(query)

        if score>0:
            hits.append((score,ds))

    hits.sort(reverse=True,key=lambda x:x[0])

    print("\nMatches:",len(hits))

    for score,ds in hits[:10]:

        print("-"*60)
        print("Dataset :",ds["dataset_id"])
        print("Name    :",ds["metadata"].get("dataset_name"))
        print("Domain  :",ds["metadata"].get("domain"))
        print("Provider:",ds["metadata"].get("provider"))
        print("Score   :",score)

print("\nSession Finished.")
