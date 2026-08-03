import pandas as pd

df=pd.read_csv(
"analysis/large_scale/results/master_amr_dataset.csv"
)

print("="*80)
print("GOHIF DATA QUALITY REPORT")
print("="*80)

print("Records:",len(df))
print("Unique genes:",df["gene"].nunique())
print("Unique pathogens:",df["pathogen"].nunique())
print("Unique drug classes:",df["drug_class"].nunique())

missing=df.isna().sum()

print()
print("Missing values")
print(missing)

missing.to_csv(
"analysis/large_scale/results/missing_values.csv"
)

df.describe(include="all").to_csv(
"analysis/large_scale/results/dataset_statistics.csv"
)
