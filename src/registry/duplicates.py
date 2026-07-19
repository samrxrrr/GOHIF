from pathlib import Path
import pandas as pd

from src.registry.loader import RegistryLoader


class DuplicateDetector:

    OUTPUT = Path(
        "metadata/registry/GOHIF_DUPLICATES.csv"
    )

    def __init__(self):

        self.loader = RegistryLoader()

    def find_duplicates(self):

        df = self.loader.load()

        duplicate_frames = []

        # Duplicate GOHIF IDs
        if "GOHIF_ID" in df.columns:
            dup = df[df.duplicated("GOHIF_ID", keep=False)]
            if not dup.empty:
                dup["Duplicate_Type"] = "GOHIF_ID"
                duplicate_frames.append(dup)

        # Duplicate Dataset Names
        if "Dataset_Name" in df.columns:
            dup = df[df.duplicated("Dataset_Name", keep=False)]
            if not dup.empty:
                dup["Duplicate_Type"] = "Dataset_Name"
                duplicate_frames.append(dup)

        # Duplicate Official Website
        if "Official_Website" in df.columns:
            temp = df[df["Official_Website"].fillna("") != ""]
            dup = temp[temp.duplicated("Official_Website", keep=False)]
            if not dup.empty:
                dup["Duplicate_Type"] = "Official_Website"
                duplicate_frames.append(dup)

        # Duplicate Download URL
        if "Download_URL" in df.columns:
            temp = df[df["Download_URL"].fillna("") != ""]
            dup = temp[temp.duplicated("Download_URL", keep=False)]
            if not dup.empty:
                dup["Duplicate_Type"] = "Download_URL"
                duplicate_frames.append(dup)

        if duplicate_frames:
            result = pd.concat(
                duplicate_frames,
                ignore_index=True
            ).drop_duplicates()

        else:
            result = pd.DataFrame()

        self.OUTPUT.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        result.to_csv(
            self.OUTPUT,
            index=False
        )

        return result


if __name__ == "__main__":

    detector = DuplicateDetector()

    duplicates = detector.find_duplicates()

    print()

    print("Duplicate Records :", len(duplicates))

    if not duplicates.empty:

        print()

        print(
            duplicates[
                [
                    "GOHIF_ID",
                    "Dataset_Name",
                    "Duplicate_Type"
                ]
            ]
        )
