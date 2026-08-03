from pathlib import Path

ROOT=Path("analysis/large_scale/normalized")

print("="*80)
print("GOHIF NORMALIZED DATASETS")
print("="*80)

for f in ROOT.glob("*.csv"):

    print(f.name)
