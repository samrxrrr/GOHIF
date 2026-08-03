import pandas as pd


dock = pd.read_csv(
"analysis/structure_discovery/docking/results/vina_scores.csv"
)


targets = pd.read_csv(
"analysis/amr_integration/amr_target_rankings.csv"
)


print("Docking columns:")
print(dock.columns.tolist())

print("\nAMR columns:")
print(targets.columns.tolist())


# remove invalid docking
dock = dock[
    dock["binding_affinity_kcal_mol"] < 0
]


# map target IDs to pathogen
target_map = {

"GOHIF_STRUCT_0001":"Salmonella",

"GOHIF_STRUCT_0002":"Escherichia coli",

"GOHIF_STRUCT_0003":"Mycobacterium tuberculosis"

}


dock["pathogen"] = dock["target_id"].map(target_map)


merged = dock.merge(
    targets,
    on="pathogen",
    how="left"
)


merged["docking_score"] = (
    abs(
        merged["binding_affinity_kcal_mol"]
    )
)


merged["GOHIF_final_drug_score"] = (

    merged["docking_score"] * 0.5

    +

    merged["GOHIF_AMR_score"] * 0.5

)


merged = merged.sort_values(
    "GOHIF_final_drug_score",
    ascending=False
)


merged.to_csv(
"analysis/drug_discovery/final_drug_candidates.csv",
index=False
)


print("="*80)
print("GOHIF INTEGRATED DRUG PRIORITIZATION COMPLETE")
print("="*80)


print(
merged[
[
"pathogen",
"compound",
"binding_affinity_kcal_mol",
"GOHIF_AMR_score",
"GOHIF_final_drug_score"
]
].to_string(index=False)
)

