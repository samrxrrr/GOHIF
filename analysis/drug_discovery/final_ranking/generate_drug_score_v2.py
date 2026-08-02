import pandas as pd


dock = pd.read_csv(
"analysis/structure_discovery/docking/results/vina_scores.csv"
)


amr = pd.read_csv(
"analysis/amr_integration/amr_target_rankings.csv"
)


plip = pd.read_csv(
"analysis/drug_discovery/interactions/interaction_features.csv"
)


target_map = {

"GOHIF_STRUCT_0001":"Salmonella",

"GOHIF_STRUCT_0002":"Escherichia coli",

"GOHIF_STRUCT_0003":"Mycobacterium tuberculosis"

}


dock["pathogen"] = dock["target_id"].map(target_map)


# remove invalid docking
dock = dock[
dock["binding_affinity_kcal_mol"] < 0
]


merged = dock.merge(
amr,
on="pathogen",
how="left"
)


merged["complex"] = (
merged["target_id"]
+
"_"
+
merged["ligand_id"]
)


merged = merged.merge(
plip,
on="complex",
how="left"
)


merged["docking_component"] = (
abs(
merged["binding_affinity_kcal_mol"]
)
)


merged["interaction_component"] = (
merged["interaction_count"].fillna(0)
)


merged["GOHIF_drug_score_v2"] = (

merged["GOHIF_AMR_score"] * 0.5

+

merged["docking_component"] * 0.35

+

merged["interaction_component"] * 0.15

)


merged = merged.sort_values(
"GOHIF_drug_score_v2",
ascending=False
)


merged.to_csv(
"analysis/drug_discovery/final_ranking/drug_candidates_v2.csv",
index=False
)


print("="*80)
print("GOHIF DRUG PRIORITY SCORE v2 COMPLETE")
print("="*80)


print(
merged[
[
"pathogen",
"compound",
"binding_affinity_kcal_mol",
"interaction_count",
"GOHIF_AMR_score",
"GOHIF_drug_score_v2"
]
].head(15).to_string(index=False)
)

