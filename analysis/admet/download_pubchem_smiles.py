import pandas as pd
import requests

df = pd.read_csv(
    "analysis/admet/admet_candidates.csv"
)

smiles=[]

for cid in df["pubchem_cid"]:

    url = (
        f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/CanonicalSMILES/TXT"
    )

    try:
        r = requests.get(url, timeout=30)
        smiles.append(r.text.strip())
    except:
        smiles.append("NA")

df["Canonical_SMILES"] = smiles

df.to_csv(
    "analysis/admet/smiles/admet_smiles.csv",
    index=False
)

print("="*80)
print("GOHIF SMILES RETRIEVAL COMPLETE")
print("="*80)
print(df.to_string(index=False))
