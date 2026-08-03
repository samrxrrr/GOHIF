import pandas as pd

df=pd.read_csv(
"analysis/biological_annotation/target_annotations.csv"
)

df["uniprot_query"]=(
df["protein"].fillna("")+
" "+
df["pathogen"].fillna("")
).str.strip()

df[[
"pathogen",
"protein",
"uniprot_query"
]].to_csv(
"analysis/biological_annotation/uniprot_queries.csv",
index=False
)

print("="*80)
print("GOHIF UNIPROT QUERY TABLE CREATED")
print("="*80)
print(df[["protein","pathogen","uniprot_query"]].to_string(index=False))
