import pandas as pd
from scipy.stats import mannwhitneyu, kruskal

df = pd.read_csv("analysis/master/GOHIF_Master_Dataset.csv")

print("="*80)
print("GOHIF STATISTICAL ANALYSIS")
print("="*80)

# PDB vs AlphaFold
pdb = df[df["structure_status"]=="Experimental (PDB)"]["GOHIF_priority_score"]
af = df[df["structure_status"]=="AlphaFold Candidate"]["GOHIF_priority_score"]

u,p = mannwhitneyu(pdb, af, alternative="two-sided")

print("\nPDB vs AlphaFold")
print(f"U statistic : {u:.2f}")
print(f"P-value     : {p:.6e}")

# Drug class comparison
groups = [
    x["GOHIF_priority_score"].values
    for _,x in df.groupby("drug_class")
]

h,p = kruskal(*groups)

print("\nDrug Classes")
print(f"H statistic : {h:.3f}")
print(f"P-value     : {p:.6e}")

# Mechanism comparison
groups = [
    x["GOHIF_priority_score"].values
    for _,x in df.groupby("Resistance_mechanism")
]

h,p = kruskal(*groups)

print("\nMechanisms")
print(f"H statistic : {h:.3f}")
print(f"P-value     : {p:.6e}")
