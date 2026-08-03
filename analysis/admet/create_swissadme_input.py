import pandas as pd

df = pd.read_csv(
    "analysis/admet/smiles/admet_smiles.csv"
)

with open(
    "analysis/admet/smiles/swissadme_input.txt",
    "w"
) as f:

    for _, row in df.iterrows():

        f.write(
            row["Canonical_SMILES"] + "\n"
        )

print("="*80)
print("SWISSADME INPUT CREATED")
print("="*80)
print(
"analysis/admet/smiles/swissadme_input.txt"
)
