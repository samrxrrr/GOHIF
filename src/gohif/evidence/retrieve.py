import json
import pickle
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path("/mnt/g/My Drive/DATASETS")

vectorizer = pickle.load(open("processed/retrieval/tfidf.pkl","rb"))
matrix = pickle.load(open("processed/retrieval/matrix.pkl","rb"))
ids = json.load(open("processed/retrieval/metadata.json"))

metadata_cache = {}

for f in ROOT.joinpath("_metadata_semantic").glob("*.json"):
    try:
        obj = json.load(open(f,encoding="utf-8"))
        metadata_cache[obj["dataset_id"]] = obj
    except:
        pass

print("="*72)
print("GOHIF Evidence Retrieval Engine")
print("Type 'exit' to quit")
print("="*72)

while True:

    q = input("\nGOHIF> ").strip()

    if q.lower()=="exit":
        break

    vec = vectorizer.transform([q])

    scores = cosine_similarity(vec,matrix)[0]

    order = scores.argsort()[::-1][:10]

    found=False

    for idx in order:

        if scores[idx]<=0:
            continue

        ds=ids[idx]

        obj=metadata_cache.get(ds,{})

        print("\n"+"="*72)

        print("Dataset :",ds)

        print("Score   :",round(float(scores[idx]),3))

        print("Title   :",obj.get("title",""))

        print("Domain  :",obj.get("domain",""))

        print("Provider:",obj.get("provider",""))

        print("Type    :",obj.get("dataset_type",""))

        print()

        print("Diseases :",", ".join(obj.get("diseases",[])[:10]))

        print("Pathogens:",", ".join(obj.get("pathogens",[])[:10]))

        print("Species  :",", ".join(obj.get("organisms",[])[:10]))

        preview=""

        if "content" in obj:

            if isinstance(obj["content"],dict):

                preview=obj["content"].get("text","")

            elif isinstance(obj["content"],str"):

                preview=obj["content"]

        preview=preview.replace("\n"," ")[:500]

        print()

        print("Preview")

        print("-"*72)

        print(preview)

        found=True

    if not found:

        print("\nNo evidence found.")
