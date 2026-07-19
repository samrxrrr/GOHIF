from pathlib import Path
import pandas as pd


class RegistryLoader:

    DEFAULT_REGISTRY = Path(
        "metadata/registry/GOHIF_MASTER_DATASET_REGISTRY.csv"
    )

    def __init__(self, registry_path=None):

        self.registry_path = Path(registry_path) if registry_path else self.DEFAULT_REGISTRY

    def load(self):

        if not self.registry_path.exists():
            raise FileNotFoundError(self.registry_path)

        return pd.read_csv(self.registry_path)

    def dataset_count(self):

        return len(self.load())

    def domains(self):

        df = self.load()

        return sorted(df["One_Health_Domain"].dropna().unique())

    def by_domain(self, domain):

        df = self.load()

        return df[df["One_Health_Domain"] == domain]

    def providers(self):

        df = self.load()

        return df["Organization"].value_counts()
