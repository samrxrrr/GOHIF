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
        chunks[obj["chunk_id"]] = obj

question=input("Question: ").strip()

vec=vectorizer.transform([question])
scores=cosine_similarity(vec,matrix)[0]
order=scores.argsort()[::-1]

seen=set()

print("\n"+"="*80)
print("GOHIF EVIDENCE")
print("="*80)

rank=1

for idx in order:

    if scores[idx]<=0:
        continue

    m=meta[idx]

    if m["dataset_id"] in seen:
        continue

    seen.add(m["dataset_id"])

    chunk=chunks[m["chunk_id"]]

    print(f"\n[{rank}] Dataset : {m['dataset_id']}")
    print(f"Score     : {scores[idx]:.3f}")
    print(f"Chunk     : {m['chunk_id'][:8]}")
    print("-"*80)
    print(chunk["text"][:1500].replace("\n"," "))
    print("-"*80)

    rank+=1

    if rank>8:
        break

print("\n"+"="*80)
print("PROMPT FOR LLM")
print("="*80)

context=[]

rank=1
seen=set()

for idx in order:

    if scores[idx]<=0:
        continue

    m=meta[idx]

    if m["dataset_id"] in seen:
        continue

    seen.add(m["dataset_id"])

    chunk=chunks[m["chunk_id"]]

    context.append(
        f"[{rank}] ({m['dataset_id']})\n{chunk['text'][:3000]}"
    )

    rank+=1

    if rank>8:
        break

prompt=f"""
You are GOHIF AI.

Answer the following scientific question ONLY using the supplied evidence.

Question:
{question}

Evidence:

{"="*60}

{chr(10).join(context)}

{"="*60}

Instructions:

- Write a scientific answer.
- Integrate evidence across datasets.
- Do not invent information.
- Mention uncertainty if evidence is incomplete.
- Finish with a Sources section listing Dataset IDs.
"""

print(prompt)
