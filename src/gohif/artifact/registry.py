from pathlib import Path
import pandas as pd
import json


class Registry:

    def __init__(self, registry_dir):

        self.registry = Path(registry_dir)

        self.registry.mkdir(
            parents=True,
            exist_ok=True
        )

        self.index = self.registry / "registry.csv"

        if not self.index.exists():

            pd.DataFrame(
                columns=[
                    "name",
                    "phase",
                    "type",
                    "version",
                    "path"
                ]
            ).to_csv(
                self.index,
                index=False
            )

    def register(
        self,
        metadata_file
    ):

        meta = json.load(
            open(metadata_file)
        )

        df = pd.read_csv(self.index)

        df.loc[len(df)] = [

            meta["name"],

            meta["phase"],

            meta["artifact_type"],

            meta["version"],

            metadata_file

        ]

        df.to_csv(
            self.index,
            index=False
        )
