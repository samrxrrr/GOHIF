from pathlib import Path
import csv

ROOT = Path("/mnt/g/My Drive/DATASETS")
OUT = Path("catalog/dataset_catalog.csv")

OUT.parent.mkdir(exist_ok=True)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["domain", "relative_path", "extension", "size_bytes"])

    for p in ROOT.rglob("*"):
        if p.is_file():
            try:
                writer.writerow([
                    p.relative_to(ROOT).parts[0],
                    p.relative_to(ROOT),
                    p.suffix.lower(),
                    p.stat().st_size,
                ])
            except Exception:
                pass

print("Catalog written to", OUT)
