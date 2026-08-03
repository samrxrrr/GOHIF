from pathlib import Path
import pandas as pd

ROOT=Path("datasets/amr_large")

rows=[]

for db in ROOT.iterdir():

    if not db.is_dir():
        continue

    files=list(db.glob("*"))

    size=sum(f.stat().st_size for f in files if f.is_file())

    rows.append({
        "database":db.name,
        "files":len(files),
        "size_MB":round(size/1024/1024,2)
    })

out=pd.DataFrame(rows)

out.to_csv(
"analysis/large_scale/results/dataset_validation.csv",
index=False
)

print("="*80)
print("GOHIF DATASET VALIDATION")
print("="*80)
print(out.to_string(index=False))
