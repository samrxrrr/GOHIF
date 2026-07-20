"""
GOHIF Download Pipeline Runner

Builds the download plan (if needed), prepares execution paths,
runs downloads, and writes execution results.
"""

from pathlib import Path

import pandas as pd

from src.download_manager.executor import DownloadExecutor
from src.download_manager.planner import DownloadPlanner


PLAN_FILE = Path("metadata/registry/GOHIF_DOWNLOAD_PLAN.csv")
RESULT_FILE = Path("metadata/registry/GOHIF_DOWNLOAD_RESULTS.csv")
RAW_DATA_DIR = Path("data/raw")


class DownloadRunner:

    def __init__(self):

        self.planner = DownloadPlanner()
        self.executor = DownloadExecutor()

    @staticmethod
    def sanitize(text):

        text = str(text)

        invalid = '<>:"/\\|?*'

        for c in invalid:
            text = text.replace(c, "_")

        text = text.replace(" ", "_")

        return text

    def build_local_paths(self, plan):

        RAW_DATA_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        paths = []

        for _, row in plan.iterrows():

            local_path = row.get("Local_Path")

            if pd.isna(local_path) or str(local_path).strip() == "":

                adapter = str(row["Adapter"]).lower()

                dataset_id = self.sanitize(row["GOHIF_ID"])

                dataset_name = self.sanitize(row["Dataset_Name"])

                folder = RAW_DATA_DIR / adapter

                folder.mkdir(
                    parents=True,
                    exist_ok=True
                )

                filename = f"{dataset_id}_{dataset_name}"

                if adapter in ("http", "api"):
                    filename += ".dat"

                paths.append(str(folder / filename))

            else:

                paths.append(local_path)

        plan["Local_Path"] = paths

        return plan

    def run(self):

        if PLAN_FILE.exists():

            print("Using existing download plan...")

            plan = pd.read_csv(PLAN_FILE)

        else:

            print("Building download plan...")

            plan = self.planner.build()

        plan = self.build_local_paths(plan)

        plan.to_csv(
            PLAN_FILE,
            index=False
        )

        print()

        print(f"Datasets scheduled : {len(plan)}")

        print()

        results = self.executor.execute(plan)

        RESULT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        results.to_csv(
            RESULT_FILE,
            index=False
        )

        success = 0
        failed = 0

        if "success" in results.columns:

            success = int(results["success"].fillna(False).sum())
            failed = len(results) - success

        print()

        print("=" * 70)
        print("DOWNLOAD SUMMARY")
        print("=" * 70)

        print()

        print(f"Total     : {len(results)}")
        print(f"Success   : {success}")
        print(f"Failed    : {failed}")

        print()

        print(f"Results written to:")
        print(f"  {RESULT_FILE}")

        return results


def main():

    print("=" * 70)
    print("GOHIF DOWNLOAD PIPELINE")
    print("=" * 70)

    runner = DownloadRunner()

    runner.run()


if __name__ == "__main__":
    main()
