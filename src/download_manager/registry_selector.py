from pathlib import Path
import pandas as pd

from src.registry.loader import RegistryLoader


class RegistrySelector:

    def __init__(self):
        self.loader = RegistryLoader()

    def all(self):
        return self.loader.load()

    def by_domain(self, domain):
        df = self.loader.load()
        return df[df["One_Health_Domain"] == domain]

    def pending(self):
        df = self.loader.load()

        if "Downloaded" not in df.columns:
            return df

        return df[
            df["Downloaded"]
            .fillna("")
            .astype(str)
            .str.lower()
            != "yes"
        ]

    def downloadable(self):
        df = self.loader.load()

        return df[
            df["Download_URL"]
            .fillna("")
            .astype(str)
            .str.strip()
            != ""
        ]

    def automation_ready(self):
        df = self.loader.load()

        return df[
            df["Automation"]
            .fillna("")
            .astype(str)
            .str.lower()
            .isin(["yes","true","supported","automatic"])
        ]
