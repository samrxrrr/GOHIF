import pandas as pd

df=pd.read_csv("analysis/master/GOHIF_Master_Dataset.csv")

df["TVI"]=(
df["GOHIF_priority_score"]*0.7+
df["pdb_count"]*0.3
)

top=(
df.sort_values(
"TVI",
ascending=False
)
.head(100)
)

top.to_csv(
"analysis/master/Therapeutic_Vulnerability_Index.csv",
index=False
)

print(top[
[
"normalized_gene",
"drug_class",
"TVI"
]
])
