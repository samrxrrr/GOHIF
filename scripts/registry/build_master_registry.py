#!/usr/bin/env python3

import csv
from pathlib import Path

BASE = Path("metadata")

MANIFEST = BASE / "downloads" / "GOHIF_Download_Manifest.csv"
SPRINT_DIR = BASE / "expansion" / "sprint1"
OUTPUT = BASE / "registry" / "GOHIF_MASTER_DATASET_REGISTRY.csv"

rows = []
seen = set()

print("=" * 60)
print("GOHIF Registry Builder")
print("=" * 60)

# ----------------------------------------------------------
# Load production manifest
# ----------------------------------------------------------

if not MANIFEST.exists():
    raise FileNotFoundError(f"Manifest not found: {MANIFEST}")

with MANIFEST.open(newline="", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    production_headers = reader.fieldnames

    for row in reader:

        dataset_id = (
            row.get("GOHIF_ID")
            or row.get("Dataset_ID")
            or row.get("ID")
        )

        if dataset_id in seen:
            print(f"[Duplicate] {dataset_id}")
            continue

        seen.add(dataset_id)
        rows.append(row)

print(f"Loaded production manifest : {len(rows)} datasets")

# ----------------------------------------------------------
# Merge candidate registries
# ----------------------------------------------------------

for csv_file in sorted(SPRINT_DIR.glob("*.csv")):

    print(f"Merging {csv_file.name}")

    with csv_file.open(newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            candidate_id = row.get("Candidate_ID")

            if candidate_id in seen:
                continue

            seen.add(candidate_id)

            candidate = {h: "" for h in production_headers}

            candidate["GOHIF_ID"] = candidate_id
            candidate["Dataset_Name"] = row.get("Dataset_Name", "")
            candidate["Acronym"] = ""
            candidate["Dataset_Version"] = "Candidate"
            candidate["Dataset_Status"] = row.get("Verification_Status", "Pending")
            candidate["Organization"] = row.get("Provider", "")
            candidate["Country_Region"] = row.get("Country", "")
            candidate["Official_Website"] = row.get("Official_URL", "")
            candidate["License"] = row.get("Access", "")

            # IMPORTANT
            candidate["One_Health_Domain"] = "Human Health"

            candidate["Evidence_Class"] = ""
            candidate["Primary_Evidence_Layer"] = ""
            candidate["Secondary_Evidence_Layers"] = ""
            candidate["Evidence_Type"] = ""
            candidate["Tier"] = row.get("Priority", "")
            candidate["Geographic_Coverage"] = row.get("Scope", "")
            candidate["Temporal_Coverage"] = ""
            candidate["Update_Frequency"] = row.get("Update_Frequency", "")
            candidate["Data_Level"] = ""
            candidate["Metadata_Quality"] = ""
            candidate["Findable"] = ""
            candidate["Accessible"] = ""
            candidate["Interoperable"] = ""
            candidate["Reusable"] = ""
            candidate["FAIR_Maturity"] = ""
            candidate["Scientific_Strength"] = ""
            candidate["Scientific_Limitations"] = ""
            candidate["Provenance"] = ""
            candidate["GOHIF_Compatibility"] = ""
            candidate["Coverage_Function"] = ""
            candidate["Freeze_Status"] = "Candidate"
            candidate["SRR"] = ""
            candidate["Decision_ID"] = ""
            candidate["Review_Date"] = ""
            candidate["Notes"] = ""

            candidate["Download_Method"] = row.get("Download_Method", "")
            candidate["Automation"] = row.get("API", "")
            candidate["Download_URL"] = row.get("Official_URL", "")
            candidate["API_Base"] = ""
            candidate["FTP_Path"] = ""
            candidate["Git_Repo"] = ""
            candidate["CLI_Command"] = ""
            candidate["Authentication"] = ""
            candidate["Local_Path"] = ""
            candidate["Checksum"] = ""
            candidate["Downloaded"] = "No"
            candidate["Download_Status"] = row.get("Automation_Status", "Pending")
            candidate["Download_Date"] = ""
            candidate["Local_File"] = ""
            candidate["File_Size_MB"] = ""
            candidate["SHA256"] = ""
            candidate["Error_Message"] = ""

            rows.append(candidate)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=production_headers,
        extrasaction="ignore"
    )

    writer.writeheader()

    for row in rows:
        writer.writerow(row)

print("-" * 60)
print(f"Master Registry written to : {OUTPUT}")
print(f"Total datasets : {len(rows)}")
print("=" * 60)
