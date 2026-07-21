"""
GOHIF Dataset Crosswalk Generator

Phase 8.2

Creates a curated mapping between parser datasets and
registry datasets.
"""

from pathlib import Path
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

REGISTRY = ROOT / "metadata/schema/GOHIF_DATASET_REGISTRY.csv"
CANONICAL = ROOT / "metadata/schema/GOHIF_CANONICAL_METADATA.csv"

OUT_CROSSWALK = ROOT / "metadata/schema/GOHIF_DATASET_CROSSWALK.csv"
OUT_UNMATCHED_PARSER = ROOT / "metadata/schema/GOHIF_UNMATCHED_PARSER_DATASETS.csv"
OUT_UNMATCHED_REGISTRY = ROOT / "metadata/schema/GOHIF_UNMATCHED_REGISTRY_DATASETS.csv"


def normalize(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(r"\.dat$", "", text)

    text = text.replace("-", " ")
    text = text.replace("_", " ")

    text = re.sub(r"[^a-z0-9 ]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


registry = pd.read_csv(REGISTRY)
canonical = pd.read_csv(CANONICAL)

registry["Normalized"] = registry["Dataset_Name"].apply(normalize)

canonical["Parser_Dataset"] = (
    canonical["Dataset_Name"]
    .str.replace(".dat", "", regex=False)
)

canonical["Normalized"] = canonical["Parser_Dataset"].apply(normalize)

rows = []
matched_registry = set()
matched_parser = set()

for _, p in canonical.iterrows():

    parser_name = p["Parser_Dataset"]
    parser_norm = p["Normalized"]

    candidate = None

    for _, r in registry.iterrows():

        reg_norm = r["Normalized"]

        score = 0

        p_tokens = set(parser_norm.split())
        r_tokens = set(reg_norm.split())

        overlap = len(p_tokens & r_tokens)

        if overlap > score:
            score = overlap
            candidate = r

    if candidate is not None and score > 0:

        matched_registry.add(candidate["Dataset_ID"])
        matched_parser.add(parser_name)

        rows.append({

            "Parser_Dataset": parser_name,

            "Registry_Dataset_ID": candidate["Dataset_ID"],

            "Registry_Dataset_Name": candidate["Dataset_Name"],

            "Confidence": score,

            "Status": "REVIEW"

        })

    else:

        rows.append({

            "Parser_Dataset": parser_name,

            "Registry_Dataset_ID": "",

            "Registry_Dataset_Name": "",

            "Confidence": 0,

            "Status": "UNMATCHED"

        })

crosswalk = pd.DataFrame(rows)

crosswalk.sort_values(
    ["Status", "Confidence"],
    ascending=[True, False],
    inplace=True
)

crosswalk.to_csv(
    OUT_CROSSWALK,
    index=False
)

canonical[
    ~canonical["Parser_Dataset"].isin(matched_parser)
].to_csv(
    OUT_UNMATCHED_PARSER,
    index=False
)

registry[
    ~registry["Dataset_ID"].isin(matched_registry)
].to_csv(
    OUT_UNMATCHED_REGISTRY,
    index=False
)

print()
print("=" * 72)
print("GOHIF DATASET CROSSWALK")
print("=" * 72)
print()

print("Parser datasets :", len(canonical))
print("Registry datasets:", len(registry))
print()

print("Candidate mappings :", (crosswalk["Status"]=="REVIEW").sum())
print("Unmatched parser   :", (crosswalk["Status"]=="UNMATCHED").sum())
print("Unmatched registry :", len(registry)-len(matched_registry))
print()

print("Output")
print(OUT_CROSSWALK)
print(OUT_UNMATCHED_PARSER)
print(OUT_UNMATCHED_REGISTRY)
