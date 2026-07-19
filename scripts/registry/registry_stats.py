#!/usr/bin/env python3

import csv
from collections import Counter

registry = "metadata/registry/GOHIF_MASTER_DATASET_REGISTRY.csv"

with open(registry, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    domains = Counter()

    total = 0

    for row in reader:
        total += 1
        domains[row.get("Domain", "Unknown")] += 1

print("=" * 50)
print("GOHIF Registry Statistics")
print("=" * 50)

print(f"Total datasets : {total}\n")

for d, c in domains.items():
    print(f"{d:30} {c}")

print("=" * 50)
