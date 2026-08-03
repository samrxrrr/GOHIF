import pandas as pd

df = pd.read_csv(
    "analysis/large_scale/uniprot/normalized_gene_dataset.csv"
)

queries = (
    df["normalized_gene"]
    .dropna()
    .drop_duplicates()
    .sort_values()
)

queries = pd.DataFrame({
    "query": queries
})

queries.to_csv(
    "analysis/large_scale/uniprot/unique_gene_queries.csv",
    index=False
)

print("="*80)
print("GOHIF UNIQUE QUERY SET")
print("="*80)

print("Original records:", len(df))
print("Unique queries:", len(queries))

print()
print(queries.head(30).to_string(index=False))
