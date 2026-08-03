import pandas as pd
from pathlib import Path

STRUCT="analysis/large_scale/structures/structure_mapping.csv"
UNI="analysis/large_scale/uniprot/uniprot_annotations_parallel.csv"

struct=pd.read_csv(STRUCT)

if not Path(UNI).exists():
    print("UniProt annotation not finished yet.")
    raise SystemExit

uni=pd.read_csv(UNI)

uni=uni.rename(columns={
"query":"gene",
"accession":"uniprot_accession"
})

merged=struct.merge(
uni[
[
"gene",
"uniprot_accession",
"organism",
"protein_name"
]
],
on="gene",
how="left"
)

merged.to_csv(
"analysis/large_scale/structures/structure_mapping.csv",
index=False
)

print("="*80)
print("GOHIF STRUCTURE DATASET UPDATED")
print("="*80)

print()

print("Targets:",len(merged))

print("UniProt mapped:",
merged["uniprot_accession"].notna().sum())

print()

print(
merged.head(20).to_string(index=False)
)
