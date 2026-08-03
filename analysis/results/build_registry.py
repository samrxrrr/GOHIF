from pathlib import Path
import hashlib
import pandas as pd
from datetime import datetime

ROOT = Path(".")
OUT = ROOT / "analysis" / "results" / "registry"
OUT.mkdir(parents=True, exist_ok=True)

records = []

EXTENSIONS = {
    ".csv", ".tsv", ".json", ".txt",
    ".xlsx", ".parquet", ".feather",
    ".pkl", ".png", ".svg", ".pdf"
}

SKIP = {
    ".git",
    ".venv",
    "__pycache__"
}

for path in ROOT.rglob("*"):

    if not path.is_file():
        continue

    if any(part in SKIP for part in path.parts):
        continue

    if path.suffix.lower() not in EXTENSIONS:
        continue

    try:
        md5 = hashlib.md5(path.read_bytes()).hexdigest()
    except Exception:
        md5 = "NA"

    records.append({
        "file": str(path.relative_to(ROOT)),
        "extension": path.suffix.lower(),
        "size_bytes": path.stat().st_size,
        "modified": datetime.fromtimestamp(
            path.stat().st_mtime
        ).isoformat(),
        "md5": md5
    })

df = (
    pd.DataFrame(records)
    .sort_values("file")
)

df.to_csv(
    OUT / "gohif_data_registry.csv",
    index=False
)

summary = (
    df.groupby("extension")
      .size()
      .reset_index(name="count")
)

summary.to_csv(
    OUT / "registry_summary.csv",
    index=False
)

print("="*80)
print("GOHIF DATA REGISTRY CREATED")
print("="*80)
print()
print("Tracked files :", len(df))
print()
print(summary.to_string(index=False))
