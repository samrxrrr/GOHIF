import pandas as pd

df=pd.read_csv(
"analysis/admet/final_gohif_drug_scores.csv"
)

pub=df[[
"compound",
"pathogen",
"binding_affinity_kcal_mol",
"GOHIF_ADMET_score",
"GOHIF_final_score_v3"
]]

pub=pub.sort_values(
"GOHIF_final_score_v3",
ascending=False
)

pub.to_csv(
"analysis/validation/publication_table.csv",
index=False
)

print("="*80)
print("PUBLICATION TABLE CREATED")
print("="*80)
print(pub.to_string(index=False))
