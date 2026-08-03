import pandas as pd
import re

# Load prioritized proteins
df = pd.read_csv(
    "analysis/large_scale/uniprot/final_annotation.csv"
)

def family(gene):

    gene=str(gene)

    rules=[

        ("OXA",r"^OXA"),

        ("CTX-M",r"^CTX"),

        ("TEM",r"^TEM"),

        ("SHV",r"^SHV"),

        ("NDM",r"^NDM"),

        ("KPC",r"^KPC"),

        ("VIM",r"^VIM"),

        ("IMP",r"^IMP"),

        ("AAC",r"^aac"),

        ("APH",r"^aph"),

        ("ANT",r"^ant"),

        ("ERM",r"^erm"),

        ("TET",r"^tet"),

        ("MCR",r"^mcr"),

        ("QNR",r"^qnr"),

        ("VAN",r"^van")

    ]

    for name,pattern in rules:

        if re.search(pattern,gene,re.I):

            return name

    return "OTHER"

df["protein_family"]=df["normalized_gene"].apply(family)

summary=(
    df.groupby("protein_family")
      .agg(

        proteins=("normalized_gene","count"),

        unique_accessions=("accession","nunique")

      )
      .sort_values("proteins",ascending=False)
      .reset_index()
)

summary.to_csv(
"analysis/research_phase1/protein_family_atlas.csv",
index=False
)

print("="*80)
print("GOHIF PROTEIN FAMILY ATLAS")
print("="*80)
print(summary.to_string(index=False))
