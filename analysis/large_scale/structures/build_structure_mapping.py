import pandas as pd

df = pd.read_csv(
    "analysis/large_scale/resfinder/gohif_resfinder_dataset.csv"
)

out = df[[
    "gene",
    "drug_class",
    "protein"
]].copy()

out["uniprot_accession"] = ""
out["pdb_id"] = ""
out["alphafold_id"] = ""
out["structure_source"] = ""
out["structure_status"] = "pending"

out.to_csv(
    "analysis/large_scale/structures/structure_mapping.csv",
    index=False
)

print("="*80)
print("GOHIF STRUCTURE MAPPING FRAMEWORK CREATED")
print("="*80)
print()
print("Targets:", len(out))
print()
print(out.head(20).to_string(index=False))
