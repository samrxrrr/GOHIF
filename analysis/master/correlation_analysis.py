import pandas as pd
from scipy.stats import spearmanr

df = pd.read_csv("analysis/master/GOHIF_Master_Dataset.csv")

rho,p = spearmanr(
    df["pdb_count"],
    df["GOHIF_priority_score"]
)

print("="*80)
print("GOHIF CORRELATION")
print("="*80)

print(f"Spearman rho : {rho:.3f}")
print(f"P-value      : {p:.6e}")
