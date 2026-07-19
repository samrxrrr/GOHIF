from pathlib import Path
import pandas as pd

from src.registry.loader import RegistryLoader


class ScientificScorer:

    OUTPUT = Path("metadata/registry/GOHIF_SCIENTIFIC_SCORES.csv")

    def __init__(self):
        self.loader = RegistryLoader()

    @staticmethod
    def has_value(v):
        return pd.notna(v) and str(v).strip() != ""

    def score(self):

        df = self.loader.load()

        scores = []

        for _, row in df.iterrows():

            metadata = 10 if self.has_value(row.get("Description")) else 0

            provenance = 10 if self.has_value(row.get("Organization")) else 0

            documentation = 10 if self.has_value(row.get("Official_Website")) else 0

            accessibility = 10 if self.has_value(row.get("Download_URL")) else 0

            api = 10 if self.has_value(row.get("API_Available")) else 0

            versioning = 10 if self.has_value(row.get("Version")) else 0

            update = 10 if self.has_value(row.get("Update_Frequency")) else 0

            license = 10 if self.has_value(row.get("License")) else 0

            citation = 10 if self.has_value(row.get("Citation")) else 0

            identifier = 10 if self.has_value(row.get("GOHIF_ID")) else 0

            total = (
                metadata +
                provenance +
                documentation +
                accessibility +
                api +
                versioning +
                update +
                license +
                citation +
                identifier
            )

            scores.append({
                "GOHIF_ID": row["GOHIF_ID"],
                "Dataset_Name": row["Dataset_Name"],
                "Metadata": metadata,
                "Provenance": provenance,
                "Documentation": documentation,
                "Accessibility": accessibility,
                "API": api,
                "Versioning": versioning,
                "Update": update,
                "License": license,
                "Citation": citation,
                "Identifier": identifier,
                "Scientific_Score": total
            })

        out = pd.DataFrame(scores)

        out.to_csv(self.OUTPUT, index=False)

        return out


if __name__ == "__main__":
    print(ScientificScorer().score().head())
