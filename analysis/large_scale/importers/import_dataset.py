from pathlib import Path
import pandas as pd

INPUT = Path("datasets/amr_large")
OUTPUT = Path("analysis/large_scale/normalized")
OUTPUT.mkdir(parents=True, exist_ok=True)

SUPPORTED = [".csv", ".tsv", ".txt"]

summary = []

for db in INPUT.iterdir():

    if not db.is_dir():
        continue

    rows = []

    for f in db.iterdir():

        if f.suffix.lower() not in SUPPORTED:
            continue

        try:

            if f.suffix.lower()==".csv":
                df=pd.read_csv(f)

            else:
                df=pd.read_csv(f,sep="\t")

            df.columns=[str(c).strip() for c in df.columns]

            rows.append(df)

            summary.append({
                "database":db.name,
                "file":f.name,
                "rows":len(df),
                "columns":len(df.columns)
            })

        except Exception as e:

            summary.append({
                "database":db.name,
                "file":f.name,
                "rows":0,
                "columns":0
            })

    if rows:

        merged=pd.concat(rows,ignore_index=True)

        merged.to_csv(
            OUTPUT/f"{db.name}_normalized.csv",
            index=False
        )

pd.DataFrame(summary).to_csv(
    "analysis/large_scale/logs/import_summary.csv",
    index=False
)

print("="*80)
print("GOHIF MULTI-DATABASE IMPORT COMPLETE")
print("="*80)

print(pd.DataFrame(summary))
