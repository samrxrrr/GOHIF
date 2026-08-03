import pandas as pd

base = pd.read_csv(
    "analysis/large_scale/uniprot/normalized_gene_dataset.csv"
)

uni = pd.read_csv(
    "analysis/large_scale/uniprot/uniprot_annotations_parallel.csv"
)

# UniProt uses "query" = normalized gene
merged = base.merge(
    uni,
    left_on="normalized_gene",
    right_on="query",
    how="left"
)

merged.to_csv(
    "analysis/large_scale/uniprot/gohif_resfinder_annotated.csv",
    index=False
)

annotated = merged["accession"].notna().sum()
coverage = annotated / len(merged) * 100

print("="*80)
print("GOHIF FINAL ANNOTATION MERGE")
print("="*80)
print(f"Genes: {len(merged)}")
print(f"Annotated: {annotated}")
print(f"Coverage: {coverage:.2f}%")

print("\nSample annotated records:\n")
print(
    merged[
        merged["accession"].notna()
    ][[
        "gene",
        "normalized_gene",
        "accession",
        "entry"
    ]].head(20).to_string(index=False)
)
