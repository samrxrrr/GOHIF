"""
GOHIF Download Planner

Builds the download execution plan from the master registry.
"""

from pathlib import Path

import pandas as pd

from src.registry.loader import RegistryLoader
from src.download_manager.adapter_resolver import AdapterResolver

OUTPUT = Path("metadata/registry/GOHIF_DOWNLOAD_PLAN.csv")


class DownloadPlanner:

    def __init__(self):
        self.loader = RegistryLoader()

    @staticmethod
    def _yes(value):
        return str(value).strip().lower() in (
            "yes",
            "true",
            "completed",
            "downloaded",
        )

    @staticmethod
    def _priority(tier):

        tier = str(tier).strip().upper()

        mapping = {
            "CRITICAL": 1,
            "HIGH": 1,
            "T1": 1,
            "TIER 1": 1,

            "MEDIUM": 2,
            "T2": 2,
            "TIER 2": 2,

            "LOW": 3,
            "T3": 3,
            "TIER 3": 3,
        }

        return mapping.get(tier, 4)

    def build(self):

        df = self.loader.load()

        rows = []

        for _, row in df.iterrows():

            if self._yes(row.get("Download_URL", "")):
                continue

            if str(row.get("Freeze_Status", "")).strip().lower() == "frozen":
                continue

            rows.append({

                "Priority": self._priority(row.get("Tier")),

                "GOHIF_ID": row.get("GOHIF_ID"),

                "Dataset_Name": row.get("Dataset_Name"),

                "Adapter": AdapterResolver.resolve(row),

                "Tier": row.get("Tier", ""),

                "Download_Method": row.get("Download_Method", ""),

                "Download_URL": row.get("Download_URL", ""),

                "API_Base": row.get("API_Base", ""),

                "Local_Path": row.get("Local_Path", ""),

                "File_Format": row.get("File_Format", ""),

                "Status": "PENDING",
            })

        plan = pd.DataFrame(rows)

        plan = plan.sort_values(
            by=[
                "Priority",
                "Adapter",
                "GOHIF_ID",
            ]
        ).reset_index(drop=True)

        OUTPUT.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        plan.to_csv(
            OUTPUT,
            index=False,
        )

        return plan


def main():

    planner = DownloadPlanner()

    plan = planner.build()

    print("=" * 70)
    print("GOHIF DOWNLOAD PLAN")
    print("=" * 70)

    print()

    print(f"Datasets : {len(plan)}")

    print()

    print("Priority Distribution")
    print(plan["Priority"].value_counts().sort_index())

    print()

    print("Adapter Distribution")
    print(plan["Adapter"].value_counts())

    print()

    print(plan.head(20))


if __name__ == "__main__":
    main()
