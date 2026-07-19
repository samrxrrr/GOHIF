from pathlib import Path
import pandas as pd

from src.download_manager.dispatcher import DownloadDispatcher

PLAN = Path("metadata/registry/GOHIF_DOWNLOAD_PLAN.csv")


class DownloadExecutor:

    def __init__(self):

        self.plan = pd.read_csv(PLAN)

        self.dispatcher = DownloadDispatcher()

    def execute(self):

        results = []

        print("=" * 80)
        print("GOHIF EXECUTION")
        print("=" * 80)

        for _, row in self.plan.iterrows():

            result = self.dispatcher.dispatch(row)

            results.append(result)

        df = pd.DataFrame(results)

        Path("logs/downloads").mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_csv(
            "logs/downloads/execution_results.csv",
            index=False
        )

        print()

        print("=" * 80)

        print(df["Success"].value_counts())

        print()

        print("Execution results written to")

        print("logs/downloads/execution_results.csv")


def main():

    DownloadExecutor().execute()


if __name__ == "__main__":

    main()
