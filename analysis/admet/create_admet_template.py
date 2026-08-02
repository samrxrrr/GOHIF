import pandas as pd

df = pd.read_csv(
    "analysis/admet/admet_candidates.csv"
)

properties = [
    "molecular_weight",
    "logP",
    "TPSA",
    "HBA",
    "HBD",
    "rotatable_bonds",
    "lipinski_pass",
    "veber_pass",
    "ghose_pass",
    "egan_pass",
    "muegge_pass",
    "GI_absorption",
    "BBB_permeability",
    "Pgp_substrate",
    "CYP1A2",
    "CYP2C9",
    "CYP2C19",
    "CYP2D6",
    "CYP3A4",
    "bioavailability_score",
    "synthetic_accessibility",
    "PAINS_alerts",
    "Brenk_alerts"
]

for col in properties:
    df[col] = ""

df.to_csv(
    "analysis/admet/admet_profiles.csv",
    index=False
)

print("="*80)
print("GOHIF ADMET TEMPLATE CREATED")
print("="*80)
print(df.head().to_string(index=False))
