"""
GOHIF Registry Enricher v2

Deterministic merge using Dataset Code extracted from parser filenames.

Example

AH-003_NCBI_Pathogen_Detection.dat

↓

AH-003

↓

GOHIF_DATASET_REGISTRY.Dataset_ID
"""

from pathlib import Path
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

REGISTRY = ROOT / "metadata/schema/GOHIF_DATASET_REGISTRY.csv"
CANONICAL = ROOT / "metadata/schema/GOHIF_CANONICAL_METADATA.csv"

OUTPUT = ROOT / "metadata/schema/GOHIF_ENRICHED_METADATA.csv"


def extract_dataset_code(name: str):

    if pd.isna(name):
        return None

    m = re.match(r"^([A-Z]{2}-\d{3})", str(name))

    if m:
        return m.group(1)

    return None


class RegistryEnricher:

    def __init__(self):

        self.registry = pd.read_csv(REGISTRY)

        self.canonical = pd.read_csv(CANONICAL)

    def prepare(self):

        self.canonical["Registry_Key"] = (
            self.canonical["Dataset_Name"]
            .apply(extract_dataset_code)
        )

    def merge(self):

        merged = self.canonical.merge(

            self.registry,

            left_on="Registry_Key",

            right_on="Dataset_ID",

            how="left",

            suffixes=("", "_Registry")

        )

        return merged

    def save(self, df):

        df.to_csv(
            OUTPUT,
            index=False
        )

    def report(self, df):

        matched = int(
            df["Dataset_ID"]
            .notna()
            .sum()
        )

        unmatched = len(df) - matched

        print()
        print("="*72)
        print("GOHIF REGISTRY ENRICHMENT V2")
        print("="*72)
        print()

        print("Registry rows  :", len(self.registry))
        print("Canonical rows :", len(self.canonical))
        print("Merged rows    :", len(df))
        print()

        print("Matched        :", matched)
        print("Unmatched      :", unmatched)

        print()

        print("Match Rate     : {:.2f}%".format(
            matched/len(df)*100
        ))

        if unmatched:

            print()
            print("="*72)
            print("FIRST UNMATCHED DATASETS")
            print("="*72)

            print(

                df[
                    df["Dataset_ID"].isna()
                ][
                    [
                        "Dataset_Name",
                        "Registry_Key"
                    ]
                ].head(20).to_string(index=False)

            )

    def run(self):

        self.prepare()

        merged = self.merge()

        self.save(merged)

        self.report(merged)


if __name__ == "__main__":

    RegistryEnricher().run()

