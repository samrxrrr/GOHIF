from pathlib import Path
import pandas as pd

from src.registry.loader import RegistryLoader


class RegistryNormalizer:

    OUTPUT = Path(
        "metadata/registry/GOHIF_NORMALIZED.csv"
    )

    def __init__(self):

        self.loader = RegistryLoader()

    def normalize(self):

        df = self.loader.load()

        # Remove leading/trailing spaces
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = (
                    df[col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

        # Standardize empty values
        df.replace(
            {
                "NA": "",
                "N/A": "",
                "None": "",
                "null": "",
                "NULL": "",
            },
            inplace=True,
        )

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Sort by GOHIF_ID
        if "GOHIF_ID" in df.columns:
            df = df.sort_values("GOHIF_ID")

        self.OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.OUTPUT, index=False)

        return df

    def summary(self):

        df = self.normalize()

        return {
            "datasets": len(df),
            "columns": len(df.columns),
            "domains": df["One_Health_Domain"].nunique(),
            "providers": df["Organization"].nunique(),
        }


if __name__ == "__main__":

    n = RegistryNormalizer()

    print(n.summary())
