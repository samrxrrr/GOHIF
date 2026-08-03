import pandas as pd

base=pd.read_csv(
"analysis/biological_annotation/target_annotations.csv"
)

hits=pd.read_csv(
"analysis/biological_annotation/uniprot_hits.csv"
)

merged=base.merge(
hits,
on=["protein","pathogen"],
how="left"
)

merged.to_csv(
"analysis/biological_annotation/annotated_targets.csv",
index=False
)

print("="*80)
print("GOHIF BIOLOGICAL ANNOTATION COMPLETE")
print("="*80)

print(
merged[
[
"pathogen",
"protein",
"accession",
"entry"
]
].to_string(index=False)
)
