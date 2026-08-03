import re
import pandas as pd

INPUT="analysis/large_scale/resfinder/gohif_resfinder_dataset.csv"
OUTPUT="analysis/large_scale/uniprot/normalized_gene_dataset.csv"
QUERY_OUTPUT="analysis/large_scale/uniprot/unique_gene_queries.csv"

df=pd.read_csv(INPUT)

def normalize(gene):

    gene=str(gene).strip()

    # Remove leading bla prefix
    gene=re.sub(r'^bla','',gene)

    # Remove accession suffixes such as
    # _AB123456
    # _NC000913
    # _CP012345
    # _AY123456
    # _EU123456
    gene=re.sub(
        r'_[A-Z]{1,6}[0-9]{4,}.*$',
        '',
        gene
    )

    # Remove allele counter
    gene=re.sub(
        r'_[0-9]+$',
        '',
        gene
    )

    # Remove "-like"
    gene=re.sub(
        r'-like.*$',
        '',
        gene,
        flags=re.IGNORECASE
    )

    # Remove trailing underscores
    gene=re.sub(
        r'_+$',
        '',
        gene
    )

    # Collapse multiple underscores
    gene=re.sub(
        r'__+',
        '_',
        gene
    )

    # Remove spaces
    gene=gene.strip()

    return gene

df["normalized_gene"]=df["gene"].apply(normalize)

df.to_csv(
    OUTPUT,
    index=False
)

queries=(
    df["normalized_gene"]
    .dropna()
    .drop_duplicates()
    .sort_values()
)

queries=pd.DataFrame({
    "query":queries
})

queries.to_csv(
    QUERY_OUTPUT,
    index=False
)

print("="*80)
print("GOHIF GENE NORMALIZATION v2 COMPLETE")
print("="*80)

print()

print("Original genes :",len(df))
print("Unique queries :",len(queries))

print()

print("Examples")
print("-"*80)

print(
df[
[
"gene",
"normalized_gene"
]
].head(40).to_string(index=False)
)

print()

print("="*80)
print("TOP 40 UNIQUE QUERIES")
print("="*80)

print(
queries.head(40).to_string(index=False)
)
