"""
GOHIF Dataset Registry Builder
Phase 4

Builds the canonical dataset registry from the
PHASE3_MASTER_INVENTORY_FREEZE.csv
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

inventory = pd.read_csv(
    "metadata/freeze/PHASE3_MASTER_INVENTORY_FREEZE.csv"
)

records = []

for _, row in inventory.iterrows():

    local_path = row.get("Local_Path")

    relative_path = None

    if pd.notna(local_path):

        local_path = str(local_path).replace("\\", "/")

        if "data/raw/" in local_path:

            relative_path = local_path.split("data/raw/",1)[1]

        else:

            relative_path = local_path

    records.append({

        "Dataset_ID"       : row["GOHIF_ID"],

        "Dataset_Name"     : row["Dataset_Name"],

        "Domain"           : row["One_Health_Domain"],

        "Source"           : row["Organization"],

        "Repository"       : row["Official_Website"],

        "Status"           : row["Dataset_Status"],

        "Downloaded"       : row["Downloaded"],

        "Relative_Path"    : relative_path,

        "Version"          : row["Dataset_Version"],

        "License"          : row["License"],

        "Citation"         : row["Provenance"],

        "Created_UTC"      : datetime.utcnow().isoformat()

    })

df = pd.DataFrame(records)

out = Path(
    "metadata/schema/GOHIF_DATASET_REGISTRY.csv"
)

out.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    out,
    index=False
)

print("="*80)
print("GOHIF DATASET REGISTRY")
print("="*80)

print()

print("Datasets :",len(df))

print()

print("Downloaded :",df["Downloaded"].sum())

print()

print("Relative Paths :",df["Relative_Path"].notna().sum())

print()

print("Saved :",out)
