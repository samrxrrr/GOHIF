import json
import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer

CHUNKS = Path("processed/chunks/chunks.jsonl")

docs = []
meta = []

with open(CHUNKS, encoding="utf-8") as f:

    for line in f:

        obj = json.loads(line)

        docs.append(obj["text"])

        meta.append({
            "chunk_id": obj["chunk_id"],
            "dataset_id": obj["dataset_id"],
            "title": obj["title"]
        })

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=100000,
    ngram_range=(1,2)
)

matrix = vectorizer.fit_transform(docs)

OUT = Path("processed/chunk_retrieval")
OUT.mkdir(exist_ok=True)

pickle.dump(vectorizer, open(OUT/"tfidf.pkl","wb"))
pickle.dump(matrix, open(OUT/"matrix.pkl","wb"))

json.dump(meta,
          open(OUT/"metadata.json","w"),
          indent=2)

print("="*70)
print("GOHIF Chunk Retrieval Index")
print("="*70)
print("Chunks     :",len(docs))
print("Vocabulary :",len(vectorizer.vocabulary_))
