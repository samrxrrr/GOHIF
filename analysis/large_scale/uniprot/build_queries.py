import pandas as pd

df=pd.read_csv(
"analysis/large_scale/resfinder/gohif_resfinder_dataset.csv"
)

queries=df[[
"gene",
"drug_class"
]].copy()

queries["query"]=queries["gene"]

queries.to_csv(
"analysis/large_scale/uniprot/uniprot_queries.csv",
index=False
)

print("="*80)
print("GOHIF UNIPROT QUERY DATASET")
print("="*80)

print("Queries:",len(queries))

print(queries.head(20).to_string(index=False))
