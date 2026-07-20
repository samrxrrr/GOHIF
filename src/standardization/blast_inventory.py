"""
GOHIF Phase 3
BLAST Database Inventory Builder

Groups BLAST component files into logical databases.
"""

from pathlib import Path
import pandas as pd

BLAST_EXTENSIONS = {
    ".nhr", ".nin", ".nsq",
    ".phr", ".pin", ".psq",
    ".ndb", ".not", ".ntf", ".nto", ".njs",
    ".pdb", ".pot", ".pto", ".ptf", ".pjs"
}

ROOT = Path("data/raw")

records = {}

for f in ROOT.rglob("*"):

    if not f.is_file():
        continue

    if f.suffix.lower() not in BLAST_EXTENSIONS:
        continue

    key = str(f.parent / f.stem)

    if key not in records:
        records[key] = {
            "Database_Name": f.stem,
            "Directory": str(f.parent.relative_to(ROOT)),
            "Component_Count": 0,
            "Total_Size_MB": 0.0,
            "Components": []
        }

    records[key]["Component_Count"] += 1

    records[key]["Total_Size_MB"] += (
        f.stat().st_size / 1024 / 1024
    )

    records[key]["Components"].append(f.suffix.lower())

df = pd.DataFrame(records.values())

df["Total_Size_MB"] = df["Total_Size_MB"].round(3)

df["Components"] = df["Components"].apply(
    lambda x: ",".join(sorted(x))
)

out = Path(
    "metadata/schema/BLAST_DATABASE_INVENTORY.csv"
)

out.parent.mkdir(parents=True, exist_ok=True)

df = df.sort_values(
    ["Directory", "Database_Name"]
)

df.to_csv(out, index=False)

print("=" * 80)
print("GOHIF BLAST DATABASE INVENTORY")
print("=" * 80)
print()

print("Logical Databases :", len(df))
print()

print(df.head(10))

print()

print("Saved :", out)
