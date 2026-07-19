#!/usr/bin/env python3

import shutil
from pathlib import Path
from datetime import date
import pandas as pd

MASTER = Path("datasets/master_inventory/Master_Dataset_Inventory_v2.csv")
PLANT = Path("datasets/final_registry/PlantHealth_Final.csv")
GENOMICS = Path("datasets/final_registry/Genomics_Final.csv")

if not MASTER.exists():
    raise FileNotFoundError(MASTER)

backup = MASTER.with_suffix(".backup.csv")
shutil.copy2(MASTER, backup)
print(f"Backup created: {backup}")

master = pd.read_csv(MASTER)

required_cols = list(master.columns)

def convert(df):
    rows = []

    for _, r in df.iterrows():

        domain = r["Domain"]

        if domain == "Plant Health":
            evidence_layer = "Plant Health"
        elif domain == "Genomics":
            evidence_layer = "Genomics & Molecular Evidence"
        else:
            evidence_layer = domain

        row = {
            "GOHIF_ID": r["GOHIF_ID"],
            "Dataset_Name": r["Dataset"],
            "Acronym": "",
            "Dataset_Version": r["Version"],
            "Dataset_Status": r["Status"],
            "Organization": r["Organization"],
            "Country_Region": "International",
            "Official_Website": r["Source_URL"],
            "License": "To be verified",
            "One_Health_Domain": domain,
            "Evidence_Class": "Primary",
            "Primary_Evidence_Layer": evidence_layer,
            "Secondary_Evidence_Layers": "",
            "Evidence_Type": r["Category"],
            "Tier": r["Tier"],
            "Geographic_Coverage": "Global",
            "Temporal_Coverage": "Current",
            "Update_Frequency": "Variable",
            "Data_Level": "Repository",
            "Metadata_Quality": "High",
            "Findable": "Yes",
            "Accessible": "Yes",
            "Interoperable": "Pending",
            "Reusable": "Pending",
            "FAIR_Maturity": "Under Assessment",
            "Scientific_Strength": "High-quality curated resource",
            "Scientific_Limitations": "To be documented",
            "Provenance": r["Organization"],
            "GOHIF_Compatibility": "High",
            "Coverage_Function": "Evidence Integration",
            "Freeze_Status": "Pending",
            "SRR": "",
            "Decision_ID": "",
            "Review_Date": date.today().isoformat(),
            "Notes": "Phase 3 migration"
        }

        rows.append(row)

    return pd.DataFrame(rows)


plant = convert(pd.read_csv(PLANT))
genomics = convert(pd.read_csv(GENOMICS))

new = pd.concat([plant, genomics], ignore_index=True)

master = master[~master["GOHIF_ID"].isin(new["GOHIF_ID"])]

master = pd.concat([master, new], ignore_index=True)

master = master[required_cols]

master.to_csv(MASTER, index=False)

print()
print("Migration complete.")
print(f"Total records : {len(master)}")
print(f"Added         : {len(new)}")
print(f"Backup        : {backup}")
