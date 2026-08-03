import pandas as pd

df=pd.read_csv(
"analysis/large_scale/resfinder/resfinder_sequences.csv"
)

print("="*80)
print("GOHIF RESFINDER QC")
print("="*80)

print()

print("Genes:",len(df))

print("Drug classes:",
df["drug_class"].nunique())

print("Shortest sequence:",
df["length"].min())

print("Longest sequence:",
df["length"].max())

print()

print(df.groupby("drug_class").size().sort_values(ascending=False))
