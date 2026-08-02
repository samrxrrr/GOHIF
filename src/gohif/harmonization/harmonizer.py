from pathlib import Path
import json

from gohif.harmonization.vocabulary import (
    PROVIDER_MAP,
    DOMAIN_MAP,
    normalize,
)

INPUT = Path("/mnt/g/My Drive/DATASETS/_metadata_standardized")
OUTPUT = Path("/mnt/g/My Drive/DATASETS/_metadata_harmonized")

OUTPUT.mkdir(exist_ok=True)

count = 0

for file in sorted(INPUT.glob("GOHIF_DS_*.json")):

    with open(file, encoding="utf-8") as f:
        obj = json.load(f)

    obj["provider"] = normalize(
        PROVIDER_MAP,
        obj["provider"]
    )

    obj["domain"] = normalize(
        DOMAIN_MAP,
        obj["domain"]
    )

    with open(OUTPUT / file.name, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

    count += 1

print("=" * 70)
print("GOHIF Harmonization Complete")
print("=" * 70)
print("Datasets harmonized :", count)
print("Output directory    :", OUTPUT)
print("=" * 70)
