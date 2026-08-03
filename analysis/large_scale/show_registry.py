import pandas as pd

df=pd.read_csv(
"analysis/large_scale/config/dataset_registry.csv"
)

print("="*80)
print("GOHIF DATASET REGISTRY")
print("="*80)
print(df.to_string(index=False))
