from pathlib import Path
import pandas as pd

from src.registry.loader import RegistryLoader


class EvidenceClassifier:

    OUTPUT = Path("metadata/registry/GOHIF_EVIDENCE_SUMMARY.csv")

    def __init__(self):
        self.loader = RegistryLoader()

    def summarize(self):

        df = self.loader.load()

        summary = (
            df.groupby(
                [
                    "One_Health_Domain",
                    "Primary_Evidence_Layer"
                ]
            )
            .size()
            .reset_index(name="Datasets")
            .sort_values(
                [
                    "One_Health_Domain",
                    "Datasets"
                ],
                ascending=[True, False]
            )
        )

        self.OUTPUT.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        summary.to_csv(
            self.OUTPUT,
            index=False
        )

        return summary


if __name__ == "__main__":

    print(EvidenceClassifier().summarize())
