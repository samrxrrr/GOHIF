import pandas as pd

df = pd.read_csv(
    "analysis/master/GOHIF_Master_Dataset.csv"
)

drug = (
    df.groupby("drug_class")
      .agg(
          Proteins=("normalized_gene","count"),
          MeanPriority=("GOHIF_priority_score","mean")
      )
      .sort_values("Proteins",ascending=False)
)

drug.to_csv(
    "analysis/master/Drug_Class_Landscape.csv"
)

print(drug)
