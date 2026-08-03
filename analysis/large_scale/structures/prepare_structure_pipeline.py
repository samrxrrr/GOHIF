import pandas as pd

df=pd.read_csv(
"analysis/large_scale/structures/structure_mapping.csv"
)

summary=pd.DataFrame({

"Metric":[

"Total genes",

"Unique drug classes",

"Structure status pending"

],

"Value":[

len(df),

df["drug_class"].nunique(),

(df["structure_status"]=="pending").sum()

]

})

summary.to_csv(
"analysis/large_scale/structures/structure_pipeline_summary.csv",
index=False
)

print("="*80)
print("GOHIF STRUCTURE PIPELINE READY")
print("="*80)
print(summary.to_string(index=False))
