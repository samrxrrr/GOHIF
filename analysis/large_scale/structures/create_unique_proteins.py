import pandas as pd

df = pd.read_csv(
    "analysis/large_scale/uniprot/gohif_resfinder_annotated.csv"
)

df = df.dropna(subset=["accession"])

unique = (
    df
    .drop_duplicates(subset=["accession"])
    .sort_values("accession")
)

unique.to_csv(
    "analysis/large_scale/structures/unique_proteins.csv",
    index=False
)

print("="*80)
print("GOHIF UNIQUE PROTEIN ATLAS")
print("="*80)

print(f"Annotated genes : {len(df)}")
print(f"Unique proteins : {len(unique)}")
print(f"Redundancy removed : {len(df)-len(unique)}")

print("\nTop proteins:\n")

cols = ["normalized_gene","accession"]
if "recommended_name" in unique.columns:
    cols.append("recommended_name")
elif "protein_name" in unique.columns:
    cols.append("protein_name")

print(unique[cols].head(30).to_string(index=False))
