import pandas as pd

df = pd.read_csv("analysis/master/GOHIF_Master_Dataset.csv")

out = (
    df.groupby("organism")
      .agg(
          Proteins=("normalized_gene","count"),
          MeanPriority=("GOHIF_priority_score","mean"),
          ExperimentalStructures=("pdb_count",lambda x:(x>0).sum())
      )
      .sort_values("Proteins",ascending=False)
)

out.to_csv(
"analysis/master/Pathogen_Landscape.csv"
)

print(out.head(30))
