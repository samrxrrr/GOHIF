from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer

CORPUS = Path("processed/corpus/corpus.jsonl")

OUT_DIR = Path("processed/embeddings")
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "BAAI/bge-small-en-v1.5"

print("="*70)
print("Loading embedding model...")
print("="*70)

model = SentenceTransformer(MODEL_NAME)

vectors = []
metadata = []

with open(CORPUS, encoding="utf-8") as f:

    for line in f:

        obj = json.loads(line)

        text = obj["text"].strip()

        if not text:
            continue

        embedding = model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        vectors.append(embedding)

        metadata.append({
            "dataset_id": obj["dataset_id"]
        })

vectors = np.array(vectors, dtype=np.float32)

np.save(
    OUT_DIR / "embeddings.npy",
    vectors
)

with open(
    OUT_DIR / "metadata.json",
    "w",
    encoding="utf-8"
) as fp:

    json.dump(metadata, fp, indent=2)

print("="*70)
print("GOHIF Embedding Generation Complete")
print("="*70)
print("Documents :", len(metadata))
print("Dimension :", vectors.shape[1])
print("Output    :", OUT_DIR)
print("="*70)
