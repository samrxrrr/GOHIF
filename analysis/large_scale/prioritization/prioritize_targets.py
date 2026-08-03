import pandas as pd

df = pd.read_csv(
    "analysis/large_scale/qc/high_confidence_amr_proteins.csv"
)

pdb = pd.read_csv(
    "analysis/large_scale/pdb/pdb_mapping.csv"
)

# Keep one record per UniProt accession
pdb = (
    pdb.groupby("accession", as_index=False)["pdb_count"]
       .max()
)

df = df.merge(
    pdb,
    on="accession",
    how="left"
)

df["pdb_count"] = df["pdb_count"].fillna(0)

drug_bonus = {
    "beta-lactam":5,
    "carbapenem":5,
    "aminoglycoside":4,
    "colistin":5,
    "macrolide":3,
    "tetracycline":3,
    "fluoroquinolone":3
}

df["drug_bonus"] = (
    df["drug_class"]
      .map(drug_bonus)
      .fillna(2)
)

df["GOHIF_priority_score"] = (
    5 +
    df["drug_bonus"] +
    df["pdb_count"]*2
)

# Remove duplicate proteins
df = (
    df.sort_values(
        "GOHIF_priority_score",
        ascending=False
    )
    .drop_duplicates(subset=["accession"])
)

df.to_csv(
    "analysis/large_scale/prioritization/prioritized_targets.csv",
    index=False
)

print("="*80)
print("GOHIF TARGET PRIORITIZATION v2")
print("="*80)
print()

print("Unique proteins:",len(df))

print()

print(df[
[
"normalized_gene",
"accession",
"drug_class",
"pdb_count",
"GOHIF_priority_score"
]
].head(30).to_string(index=False))
