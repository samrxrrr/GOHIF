import pandas as pd

priority = pd.read_csv("analysis/final_dataset/prioritized_targets.csv")
structure = pd.read_csv("analysis/final_dataset/structure_coverage_dataset.csv")
mechanism = pd.read_csv("analysis/final_dataset/resistance_mechanism_atlas.csv")

cols = [
    "normalized_gene",
    "organism",
    "drug_class",
    "Resistance_mechanism",
    "GOHIF_priority_score",
    "pdb_count",
    "structure_status"
]

master = (
    priority
    .merge(
        structure[["normalized_gene","structure_status"]],
        on="normalized_gene",
        how="left"
    )
    .merge(
        mechanism[["normalized_gene","Resistance_mechanism"]],
        on="normalized_gene",
        how="left"
    )
)

master = master[cols].drop_duplicates()

master.to_csv(
    "analysis/master/GOHIF_Master_Dataset.csv",
    index=False
)

print(master.head())

print()

print("Rows:",len(master))
