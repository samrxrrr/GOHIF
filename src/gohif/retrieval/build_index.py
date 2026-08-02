from pathlib import Path
import json
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer

CORPUS = Path("processed/corpus/corpus.jsonl")

OUT = Path("processed/retrieval")
OUT.mkdir(parents=True, exist_ok=True)

documents = []
metadata = []

with open(CORPUS, encoding="utf-8") as f:

    for line in f:

        obj = json.loads(line)

        documents.append(obj["text"])

        metadata.append(obj["dataset_id"])

vectorizer = TfidfVectorizer(
    stop_words="english",
    lowercase=True,
    max_features=50000
)

matrix = vectorizer.fit_transform(documents)

with open(OUT / "tfidf.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open(OUT / "matrix.pkl", "wb") as f:
    pickle.dump(matrix, f)

with open(OUT / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("="*70)
print("GOHIF TF-IDF Index Built")
print("="*70)
print("Documents :", len(metadata))
print("Vocabulary:", len(vectorizer.vocabulary_))
print("="*70)
