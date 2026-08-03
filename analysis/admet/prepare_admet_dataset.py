import pandas as pd

drug = pd.read_csv(
    "analysis/drug_discovery/final_ranking/drug_candidates_v2.csv"
)

cid_map = {
    "Isoniazid":3767,
    "Clavulanic acid":5280980,
    "Avibactam":9835049,
    "Colistin":5311054,
    "EDTA":6049
}

drug["pubchem_cid"] = drug["compound"].map(cid_map)

drug = drug[[
    "compound",
    "pubchem_cid",
    "pathogen",
    "GOHIF_drug_score_v2"
]]

drug = drug.drop_duplicates()

drug.to_csv(
    "analysis/admet/admet_candidates.csv",
    index=False
)

print("="*80)
print("GOHIF ADMET DATASET CREATED")
print("="*80)
print(drug.to_string(index=False))
