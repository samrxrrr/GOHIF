import json
import pickle
from pathlib import Path

from sklearn.metrics.pairwise import cosine_similarity

vectorizer = pickle.load(open("processed/chunk_retrieval/tfidf.pkl","rb"))
matrix = pickle.load(open("processed/chunk_retrieval/matrix.pkl","rb"))
meta = json.load(open("processed/chunk_retrieval/metadata.json"))

chunks = {}

with open("processed/chunks/chunks.jsonl",encoding="utf-8") as f:

    for line in f:

        obj=json.loads(line)

        chunks[obj["chunk_id"]] = obj

print("="*70)
print("GOHIF Context Builder")
print("Type exit to quit")
print("="*70)

while True:

    q=input("\nQuestion: ").strip()

    if q.lower()=="exit":
        break

    vec=vectorizer.transform([q])

    scores=cosine_similarity(vec,matrix)[0]

    order=scores.argsort()[::-1]

    context=[]

    seen=set()

    for idx in order:

        if scores[idx]<=0:
            continue

        m=meta[idx]

        if m["dataset_id"] in seen:
            continue

        seen.add(m["dataset_id"])

        chunk=chunks[m["chunk_id"]]

        context.append({
            "dataset":m["dataset_id"],
            "chunk":m["chunk_id"],
            "score":float(scores[idx]),
            "text":chunk["text"]
        })

        if len(context)==10:
            break

    Path("processed/rag").mkdir(exist_ok=True)

    outfile="processed/rag/context.json"

    json.dump(
        {
            "question":q,
            "context":context
        },
        open(outfile,"w"),
        indent=2,
        ensure_ascii=False
    )

    print()

    print("Context saved ->",outfile)

    print("Chunks:",len(context))
