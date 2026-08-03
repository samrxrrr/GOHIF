import pandas as pd

df = pd.read_csv(
    "analysis/master/GOHIF_Master_Dataset.csv"
)

df["family"] = (
    df["normalized_gene"]
      .str.extract(r"([A-Za-z\-]+)")
      .fillna("Unknown")
)

atlas = (
    df.groupby("family")
      .agg(
          proteins=("family","size"),
          mean_priority=("GOHIF_priority_score","mean"),
          pdb=("pdb_count","sum")
      )
      .sort_values("proteins",ascending=False)
)

atlas.to_csv(
    "analysis/master/Protein_Family_Atlas.csv"
)

print(atlas.head(20))
