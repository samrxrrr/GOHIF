#!/usr/bin/env python3

"""
GOHIF Master Dataset Inventory Loader

Responsibilities
----------------
1. Load Master_Dataset_Inventory_v2.csv
2. Validate schema
3. Check duplicates
4. Check missing values
5. Produce validation report
6. Export cleaned dataset
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

MASTER = ROOT / "datasets" / "master_inventory" / "Master_Dataset_Inventory_v2.csv"

OUTPUT = ROOT / "outputs"

OUTPUT.mkdir(exist_ok=True)

REQUIRED_COLUMNS = [
    "GOHIF_ID",
    "Dataset_Name",
    "Acronym",
    "Dataset_Version",
    "Dataset_Status",
    "Organization",
    "Country_Region",
    "Official_Website",
    "License",
    "One_Health_Domain",
    "Evidence_Class",
    "Primary_Evidence_Layer",
    "Secondary_Evidence_Layers",
    "Evidence_Type",
    "Tier",
    "Geographic_Coverage",
    "Temporal_Coverage",
    "Update_Frequency",
    "Data_Level",
    "Metadata_Quality",
    "Findable",
    "Accessible",
    "Interoperable",
    "Reusable",
    "FAIR_Maturity",
    "Scientific_Strength",
    "Scientific_Limitations",
    "Provenance",
    "GOHIF_Compatibility",
    "Coverage_Function",
    "Freeze_Status",
    "SRR",
    "Decision_ID",
    "Review_Date",
    "Notes"
]


def validate_columns(df):

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]

    extra = [c for c in df.columns if c not in REQUIRED_COLUMNS]

    return missing, extra


def duplicate_ids(df):

    return df[df["GOHIF_ID"].duplicated(keep=False)]


def missing_summary(df):

    return df.isna().sum().sort_values(ascending=False)


def main():

    print("=" * 60)
    print("GOHIF MASTER INVENTORY VALIDATION")
    print("=" * 60)

    if not MASTER.exists():
        raise FileNotFoundError(MASTER)

    df = pd.read_csv(MASTER)

    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    missing, extra = validate_columns(df)

    print("\nSchema")

    if missing:
        print("Missing columns")
        print(missing)
    else:
        print("All required columns present")

    if extra:
        print("Extra columns")
        print(extra)

    dup = duplicate_ids(df)

    print("\nDuplicate GOHIF IDs :", len(dup))

    if len(dup):
        dup.to_csv(
            OUTPUT / "duplicate_ids.csv",
            index=False
        )

    miss = missing_summary(df)

    miss.to_csv(
        OUTPUT / "missing_values_summary.csv"
    )

    df.to_csv(
        OUTPUT / "Master_Dataset_Inventory_Clean.csv",
        index=False
    )

    report = OUTPUT / "validation_report.txt"

    with open(report, "w") as f:

        f.write("GOHIF Validation Report\n")
        f.write("=======================\n\n")
        f.write(f"Rows: {len(df)}\n")
        f.write(f"Columns: {len(df.columns)}\n")
        f.write(f"Duplicate IDs: {len(dup)}\n")

        if missing:
            f.write("\nMissing Columns\n")
            for c in missing:
                f.write(c + "\n")

    print("\nOutputs")
    print(report)
    print(OUTPUT / "Master_Dataset_Inventory_Clean.csv")
    print(OUTPUT / "missing_values_summary.csv")

    print("\nValidation complete.")


if __name__ == "__main__":
    main()
