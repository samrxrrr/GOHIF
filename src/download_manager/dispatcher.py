"""
GOHIF Download Dispatcher
"""

import pandas as pd


class DownloadDispatcher:

    def dispatch(self, row):

        dataset = row["Dataset_Name"]

        method = row["Download_Method"]

        if pd.isna(method) or str(method).strip() == "":
            print(f"[SKIP] {dataset} (manual acquisition)")
            return None

        method = str(method).strip().upper()

        print(f"[AUTO] {dataset}")
        print(f"Method : {method}")

        return method


if __name__ == "__main__":

    df = pd.read_csv(
        "metadata/downloads/GOHIF_Download_Manifest.csv"
    )

    dispatcher = DownloadDispatcher()

    for _, row in df.iterrows():
        dispatcher.dispatch(row)
