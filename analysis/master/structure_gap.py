import pandas as pd

df = pd.read_csv("analysis/master/GOHIF_Master_Dataset.csv")

gap = (
    df.groupby("drug_class")
      .agg(
          Total=("normalized_gene","count"),
          Experimental=("pdb_count",lambda x:(x>0).sum()),
          AlphaFold=("pdb_count",lambda x:(x==0).sum())
      )
)

gap["Experimental_%"] = (
100*gap.Experimental/gap.Total
).round(1)

gap["Gap_%"] = (
100-gap["Experimental_%"]
).round(1)

gap.to_csv(
"analysis/master/Structure_Gap.csv"
)

print(gap)
