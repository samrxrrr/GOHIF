from pathlib import Path
import pandas as pd

ROOT=Path("datasets/global_amr")

rows=[]

for db in ROOT.iterdir():

    if not db.is_dir():
        continue

    raw=len(list((db/"raw").glob("*")))
    processed=len(list((db/"processed").glob("*")))

    rows.append({
        "database":db.name,
        "raw_files":raw,
        "processed_files":processed
    })

out=pd.DataFrame(rows)

out.to_csv(
"analysis/large_scale/results/global_inventory.csv",
index=False
)

print("="*80)
print("GOHIF GLOBAL INVENTORY")
print("="*80)
print(out.to_string(index=False))
