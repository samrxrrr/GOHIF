import pandas as pd

df = pd.read_csv("analysis/master/GOHIF_Master_Dataset.csv")

top = (
    df.sort_values(
        "GOHIF_priority_score",
        ascending=False
    )
    .head(50)
)

top.to_csv(
    "analysis/master/Top50_Therapeutic_Targets.csv",
    index=False
)

print(top[
    [
        "normalized_gene",
        "drug_class",
        "Resistance_mechanism",
        "GOHIF_priority_score",
        "pdb_count"
    ]
])
