"""
GOHIF Master Object Catalog Builder
Phase 3.2
"""

from pathlib import Path
import pandas as pd

from src.standardization.normalizer import normalize

schema = Path("metadata/schema")

master = pd.read_csv(schema / "MASTER_METADATA_CATALOG.csv")
master["Record_Type"] = "FILE"

blast = pd.read_csv(schema / "BLAST_DATABASE_INVENTORY.csv")

blast = blast.rename(columns={
    "Database_Name": "Filename"
})

blast["Record_Type"] = "BLAST_DATABASE"
blast["Object_Type"] = "BLAST_DATABASE"
blast["File_Class"] = "BLAST_DB"
blast["Relative_Path"] = blast["Directory"]
blast["Validation_Status"] = "VALID"

records = []

for _, row in master.iterrows():

    obj = normalize(row.to_dict())

    obj["Object_Type"] = "FILE"

    records.append(obj)

for _, row in blast.iterrows():

    obj = normalize(row.to_dict())

    obj["Object_Type"] = "BLAST_DATABASE"

    records.append(obj)

df = pd.DataFrame(records)

out = schema / "GOHIF_MASTER_OBJECT_CATALOG.csv"

df.to_csv(out, index=False)

print("="*80)
print("GOHIF MASTER OBJECT CATALOG")
print("="*80)

print()

print("Objects :", len(df))

print()

print(df["Object_Type"].value_counts())

print()

print(df["File_Class"].value_counts())

print()

print("Columns :", len(df.columns))

print()

print("Saved :", out)
