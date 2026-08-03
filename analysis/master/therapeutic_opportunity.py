import pandas as pd

df = pd.read_csv(
    "analysis/master/GOHIF_Master_Dataset.csv"
)

summary = (
    df.groupby("structure_status")
      .agg(
          Proteins=("normalized_gene","count"),
          MeanPriority=("GOHIF_priority_score","mean")
      )
)

summary.to_csv(
    "analysis/master/Therapeutic_Opportunity.csv"
)

print(summary)
