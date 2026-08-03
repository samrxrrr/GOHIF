import pandas as pd

cols=[
"database",
"dataset_name",
"version",
"download_date",
"license",
"citation",
"records",
"status"
]

pd.DataFrame(columns=cols).to_csv(
"analysis/large_scale/results/dataset_registry.csv",
index=False
)

print("="*80)
print("GOHIF DATASET REGISTRY CREATED")
print("="*80)
