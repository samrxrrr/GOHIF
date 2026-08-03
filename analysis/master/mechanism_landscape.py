import pandas as pd

df = pd.read_csv(
    "analysis/master/GOHIF_Master_Dataset.csv"
)

land = (
    df.groupby("Resistance_mechanism")
      .agg(
          Proteins=("normalized_gene","count"),
          MeanPriority=("GOHIF_priority_score","mean")
      )
      .sort_values("Proteins",ascending=False)
)

land.to_csv(
    "analysis/master/Resistance_Mechanism_Landscape.csv"
)

print(land)
