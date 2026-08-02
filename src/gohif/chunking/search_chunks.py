import json
import pickle

from sklearn.metrics.pairwise import cosine_similarity

vectorizer = pickle.load(open("processed/chunk_retrieval/tfidf.pkl","rb"))
matrix = pickle.load(open("processed/chunk_retrieval/matrix.pkl","rb"))
meta = json.load(open("processed/chunk_retrieval/metadata.json"))

chunks = {}

with open("processed/chunks/chunks.jsonl",encoding="utf-8") as f:

    for line in f:

        obj=json.loads(line)

        chunks[obj["chunk_id"]]=obj

print("="*72)
print("GOHIF Chunk Retrieval")
print("Type 'exit' to quit")
print("="*72)

while True:

    q=input("\nGOHIF> ").strip()

    if q.lower()=="exit":
        break

    vec=vectorizer.transform([q])

    scores=cosine_similarity(vec,matrix)[0]

    order=scores.argsort()[::-1]

    shown=0
    seen=set()

    for idx in order:

        if scores[idx]<=0:
            continue

        m=meta[idx]

        if m["dataset_id"] in seen:
            continue

        seen.add(m["dataset_id"])

        chunk=chunks[m["chunk_id"]]

        print("\n"+"="*72)
        print("Dataset :",m["dataset_id"])
        print("Chunk   :",m["chunk_id"][:8])
        print("Score   :",round(float(scores[idx]),3))
        print()

        print(chunk["text"][:1200].replace("\n"," "))

        shown+=1

        if shown==10:
            break

    if shown==0:
        print("\nNo evidence found.")
