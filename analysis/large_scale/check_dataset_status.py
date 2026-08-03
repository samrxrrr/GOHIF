import pandas as pd

inv=pd.read_csv(
"analysis/large_scale/results/database_inventory.csv"
)

print("="*80)
print("GOHIF DATASET INVENTORY")
print("="*80)

print(inv.to_string(index=False))

print()

print("TOTAL DATABASES:",len(inv))
print("DATABASES READY:",
      (inv["files_found"]>0).sum())
