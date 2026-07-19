#!/usr/bin/env python3

import csv
from pathlib import Path

BASE = Path("metadata")

MANIFEST = BASE / "downloads" / "GOHIF_Download_Manifest.csv"
EXPANSION = BASE / "expansion"
OUTPUT = BASE / "registry" / "GOHIF_MASTER_DATASET_REGISTRY.csv"

rows = []
seen = set()

print("=" * 60)
print("GOHIF Registry Builder")
print("=" * 60)

# ------------------------------------------------------------
# Load production manifest
# ------------------------------------------------------------

if not MANIFEST.exists():
    raise FileNotFoundError(f"Cannot find {MANIFEST}")

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
            continue

        seen.add(dataset_id)
        rows.append(row)

print(f"Loaded production manifest : {len(rows)} datasets")

# ------------------------------------------------------------
# Merge ALL sprint folders automatically
# ------------------------------------------------------------

for sprint in sorted(EXPANSION.glob("sprint*")):

    print(f"\nProcessing {sprint.name}")

    for csv_file in sorted(sprint.glob("*.csv")):

        print(f"  -> {csv_file.name}")

        with csv_file.open(newline="", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            for row in reader:

                cid = row.get("Candidate_ID")

                if not cid:
                    continue

                if cid in seen:
                    continue

                seen.add(cid)

                candidate = {h: "" for h in production_headers}

                candidate["GOHIF_ID"] = cid
                candidate["Dataset_Name"] = row.get("Dataset_Name","")
                candidate["Dataset_Version"] = "Candidate"
                candidate["Dataset_Status"] = row.get("Verification_Status","Pending")
                candidate["Organization"] = row.get("Provider","")
                candidate["Country_Region"] = row.get("Country","")
                candidate["Official_Website"] = row.get("Official_URL","")
                candidate["License"] = row.get("Access","")

                sprint_domain = {
                    "sprint1": "Human Health",
                    "sprint2": "Animal Health",
                    "sprint3": "Environmental Health",
                    "sprint4": "Food Chain",
                    "sprint5": "Plant Health",
                    "sprint6": "Genomics"
                }

                candidate["One_Health_Domain"] = sprint_domain.get(
                    sprint.name,
                    "Unknown"
                )

                candidate["Tier"] = row.get("Priority","")
                candidate["Geographic_Coverage"] = row.get("Scope","")
                candidate["Update_Frequency"] = row.get("Update_Frequency","")
                candidate["Freeze_Status"] = "Candidate"

                candidate["Download_Method"] = row.get("Download_Method","")
                candidate["Automation"] = row.get("API","")
                candidate["Download_URL"] = row.get("Official_URL","")
                candidate["Downloaded"] = "No"
                candidate["Download_Status"] = row.get("Automation_Status","Pending")

                rows.append(candidate)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=production_headers,
        extrasaction="ignore"
    )

    writer.writeheader()

    writer.writerows(rows)

print("-" * 60)
print(f"Master Registry : {OUTPUT}")
print(f"Total datasets  : {len(rows)}")
print("=" * 60)
