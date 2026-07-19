#!/usr/bin/env python3

import csv
import sys
from collections import Counter
from pathlib import Path

REGISTRY = Path("metadata/registry/GOHIF_MASTER_DATASET_REGISTRY.csv")

if not REGISTRY.exists():
    print("ERROR: Registry not found.")
    sys.exit(1)

required_columns = [
    "GOHIF_ID",
    "Dataset_Name",
    "Organization",
    "One_Health_Domain",
    "Official_Website"
]

valid_domains = {
    "Human Health",
    "Animal Health",
    "Environmental Health",
    "Food Chain",
    "Plant Health",
    "Genomics",
    "Animal Health;Food Chain"
}

ids = Counter()
names = Counter()

errors = []
warnings = []

with REGISTRY.open(newline="", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    headers = reader.fieldnames

    for col in required_columns:
        if col not in headers:
            errors.append(f"Missing required column: {col}")

    rows = list(reader)

for row_num, row in enumerate(rows, start=2):

    dataset_id = row["GOHIF_ID"].strip()
    dataset_name = row["Dataset_Name"].strip()
    organization = row["Organization"].strip()
    domain = row["One_Health_Domain"].strip()
    website = row["Official_Website"].strip()

    ids[dataset_id] += 1
    names[dataset_name] += 1

    if dataset_id == "":
        errors.append(f"Row {row_num}: Missing GOHIF_ID")

    if dataset_name == "":
        errors.append(f"Row {row_num}: Missing Dataset_Name")

    if organization == "":
        warnings.append(f"Row {row_num}: Missing Organization")

    if website == "":
        warnings.append(f"Row {row_num}: Missing Official_Website")

    if domain not in valid_domains:
        warnings.append(
            f"Row {row_num}: Unknown domain '{domain}'"
        )

for dataset_id, count in ids.items():
    if count > 1:
        errors.append(
            f"Duplicate GOHIF_ID: {dataset_id}"
        )

for dataset_name, count in names.items():
    if count > 1:
        warnings.append(
            f"Duplicate Dataset_Name: {dataset_name}"
        )

print("="*70)
print("GOHIF Registry Validation Report")
print("="*70)

print(f"Datasets checked : {len(rows)}")
print(f"Unique IDs       : {len(ids)}")

print()

print(f"Errors   : {len(errors)}")
print(f"Warnings : {len(warnings)}")

print()

if errors:
    print("ERRORS")
    print("-"*70)
    for e in errors:
        print(e)

if warnings:
    print()
    print("WARNINGS")
    print("-"*70)
    for w in warnings:
        print(w)

print()

if len(errors)==0:
    print("Registry validation PASSED")
else:
    print("Registry validation FAILED")
