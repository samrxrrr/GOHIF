import pandas as pd

df=pd.read_csv(
"analysis/large_scale/structures/structure_mapping.csv"
)

queries=df[[
"gene",
"drug_class"
]].copy()

queries.to_csv(
"analysis/large_scale/structures/pdb_queries.csv",
index=False
)

print("="*80)
print("GOHIF PDB QUERY DATASET CREATED")
print("="*80)

print()

print("Queries:",len(queries))

print()

print(
queries.head(20).to_string(index=False)
)
