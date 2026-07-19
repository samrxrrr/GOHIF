#!/usr/bin/env python3

import csv
from collections import Counter

registry = "metadata/registry/GOHIF_MASTER_DATASET_REGISTRY.csv"

with open(registry, newline="", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    headers = reader.fieldnames

    print("=" * 60)
    print("GOHIF Registry Statistics")
    print("=" * 60)

    print("\nDetected Columns:\n")

    for h in headers:
        print(" -", h)

    print()

    possible_columns = [
        "Domain",
        "Domains",
        "Primary_Domain",
        "Scientific_Domain",
        "One_Health_Domain",
        "Dataset_Domain",
        "Coverage_Domain",
        "Scope"
    ]

    domain_column = None

    for c in possible_columns:
        if c in headers:
            domain_column = c
            break

    print(f"Using domain column: {domain_column}\n")

    counter = Counter()

    total = 0

    for row in reader:

        total += 1

        if domain_column:
            value = row.get(domain_column, "").strip()
        else:
            value = "Unknown"

        if value == "":
            value = "Unknown"

        counter[value] += 1

print(f"Total datasets : {total}\n")

for k, v in counter.most_common():
    print(f"{k:35} {v}")

print("=" * 60)
