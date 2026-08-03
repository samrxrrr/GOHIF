from pathlib import Path
import pandas as pd

sources = {
    "CARD": "datasets/amr_large/CARD",
    "ResFinder": "datasets/amr_large/ResFinder",
    "NCBI": "datasets/amr_large/NCBI",
    "WHO": "datasets/amr_large/WHO"
}

summary=[]

for name,path in sources.items():

    p=Path(path)

    files=list(p.glob("*.csv"))+list(p.glob("*.tsv"))

    summary.append({
        "database":name,
        "files_found":len(files)
    })

pd.DataFrame(summary).to_csv(
"analysis/large_scale/results/database_inventory.csv",
index=False
)

print("="*80)
print("GOHIF LARGE SCALE IMPORT ENGINE READY")
print("="*80)
print(pd.DataFrame(summary).to_string(index=False))
