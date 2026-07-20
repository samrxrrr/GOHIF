"""
GOHIF Dataset Object Relationship Builder
Phase 4.1

Creates:
metadata/schema/GOHIF_DATASET_OBJECT_MAP.csv
"""

from pathlib import Path
import uuid
import pandas as pd

SCHEMA = Path("metadata/schema")

dataset_df = pd.read_csv(
    SCHEMA / "GOHIF_DATASET_REGISTRY.csv"
)

object_df = pd.read_csv(
    SCHEMA / "GOHIF_MASTER_OBJECT_CATALOG.csv"
)

# ----------------------------------------------------------------------
# Dataset lookup
# ----------------------------------------------------------------------

dataset_lookup = {}

for _, row in dataset_df.iterrows():

    rel = row.get("Relative_Path")

    if pd.notna(rel):

        rel = str(rel).strip().replace("\\","/")

        dataset_lookup[rel] = row

records = []

# ----------------------------------------------------------------------
# Object -> Dataset Mapping
# ----------------------------------------------------------------------

for _, obj in object_df.iterrows():

    obj_path = str(
        obj["Relative_Path"]
    ).strip().replace("\\","/")

    matched = None

    best_length = -1

    for dataset_path, dataset in dataset_lookup.items():

        if obj_path.startswith(dataset_path):

            if len(dataset_path) > best_length:

                matched = dataset

                best_length = len(dataset_path)

    if matched is None:

        continue

    records.append({

        "Relationship_ID":
            str(uuid.uuid4()),

        "Dataset_ID":
            matched["Dataset_ID"],

        "Dataset_Name":
            matched["Dataset_Name"],

        "Object_ID":
            obj["Object_ID"],

        "Object_Type":
            obj["Object_Type"],

        "File_Class":
            obj["File_Class"],

        "Relative_Path":
            obj["Relative_Path"]

    })

mapping = pd.DataFrame(records)

if mapping.empty:

    print("="*80)
    print("NO RELATIONSHIPS CREATED")
    print("="*80)
    exit()

mapping = mapping.sort_values(
    [
        "Dataset_Name",
        "Object_Type",
        "File_Class"
    ]
)

out = SCHEMA / "GOHIF_DATASET_OBJECT_MAP.csv"

mapping.to_csv(
    out,
    index=False
)

print("="*80)
print("GOHIF DATASET OBJECT MAP")
print("="*80)

print()

print("Relationships :", len(mapping))

print("Datasets Connected :", mapping["Dataset_ID"].nunique())

print("Objects Connected :", mapping["Object_ID"].nunique())

print()

print(mapping.head(15))

print()

print("Saved :", out)
