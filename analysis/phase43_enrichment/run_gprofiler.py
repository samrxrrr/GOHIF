import pandas as pd
from gprofiler import GProfiler

df=pd.read_csv(
"analysis/large_scale/prioritization/prioritized_targets.csv"
)

genes=(
df["normalized_gene"]
.dropna()
.drop_duplicates()
.tolist()
)

gp=GProfiler(return_dataframe=True)

print("="*80)
print("Running GOHIF Functional Enrichment")
print("="*80)

results=gp.profile(
organism="hsapiens",
query=genes
)

results.to_csv(
"analysis/phase43_enrichment/gprofiler_results.csv",
index=False
)

print()

print("Total enriched terms:",len(results))

print()

print(
results[
[
"source",
"native",
"name",
"p_value"
]
].head(30).to_string(index=False)
)
