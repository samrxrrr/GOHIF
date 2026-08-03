import pandas as pd

targets=pd.read_csv(
"analysis/amr_integration/amr_target_rankings.csv"
)

cols=[
"uniprot_id",
"gene_symbol",
"protein_name",
"organism",
"protein_family",
"molecular_function",
"biological_process",
"cellular_component",
"go_terms",
"kegg_pathway",
"resistance_mechanism",
"subcellular_location",
"essential_gene",
"virulence_factor",
"literature_support",
"annotation_status"
]

for c in cols:
    targets[c]=""

targets["annotation_status"]="pending"

targets.to_csv(
"analysis/biological_annotation/target_annotations.csv",
index=False
)

print("="*80)
print("GOHIF BIOLOGICAL ANNOTATION FRAMEWORK CREATED")
print("="*80)
print(targets.head().to_string(index=False))
