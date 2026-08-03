import pandas as pd
from pathlib import Path


class ArtifactLoader:

    def __init__(self):

        self.registry = pd.read_csv(
            "analysis/results/registry/registry.csv"
        )

    def list(self):

        return self.registry

    def load(self,name):

        row = self.registry[
            self.registry["name"]==name
        ].iloc[0]

        metadata = Path(row["path"])

        csv = metadata.with_suffix("").with_suffix(".csv")

        return pd.read_csv(csv)
