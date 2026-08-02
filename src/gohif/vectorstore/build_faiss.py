from pathlib import Path
import json
import faiss
import numpy as np

EMBED_DIR = Path("processed/embeddings")
OUT_DIR = Path("processed/vectorstore")

OUT_DIR.mkdir(parents=True, exist_ok=True)

vectors = np.load(
    EMBED_DIR / "embeddings.npy"
).astype("float32")

index = faiss.IndexFlatIP(
    vectors.shape[1]
)

index.add(vectors)

faiss.write_index(
    index,
    str(OUT_DIR / "gohif.index")
)

with open(
    EMBED_DIR / "metadata.json",
    encoding="utf-8"
) as f:

    meta = json.load(f)

with open(
    OUT_DIR / "metadata.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(meta, f, indent=2)

print("="*70)
print("GOHIF Vector Database Built")
print("="*70)
print("Vectors :", index.ntotal)
print("Dimension :", vectors.shape[1])
print("Output :", OUT_DIR)
print("="*70)
