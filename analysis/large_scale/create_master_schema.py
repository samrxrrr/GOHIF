import pandas as pd

cols=[
"database",
"gene",
"protein",
"pathogen",
"taxonomy",
"drug_class",
"resistance_mechanism",
"sequence_identity",
"coverage",
"reference",
"evidence",
"source_version"
]

pd.DataFrame(columns=cols).to_csv(
"analysis/large_scale/results/master_amr_schema.csv",
index=False
)

print("="*80)
print("GOHIF MASTER AMR SCHEMA CREATED")
print("="*80)
print(cols)
