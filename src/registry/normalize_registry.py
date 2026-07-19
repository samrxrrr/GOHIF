from pathlib import Path
import pandas as pd

REGISTRY = Path(
    "metadata/registry/GOHIF_MASTER_DATASET_REGISTRY_ENRICHED.csv"
)

OUTPUT = Path(
    "metadata/registry/GOHIF_MASTER_DATASET_REGISTRY_NORMALIZED.csv"
)


METHOD_MAP = {

    "REST_API": "API",
    "API": "API",
    "ENA_API": "API",

    "HTTP": "HTTP",

    "REPOSITORY": "Git",

    "CLI": "CLI",

    "NCBI_DATASETS_CLI": "NCBI",

    "SRA_TOOLKIT": "SRA",

    "Manual": "Manual"
}


AUTO_MAP = {

    "Yes": "Automatic",

    "Full": "Automatic",

    "No": "Automatic",

    "Manual": "Manual"
}


class RegistryNormalizer:

    def __init__(self):

        self.df = pd.read_csv(REGISTRY)
    def normalize_download_method(self):

        self.df["Download_Method"] = (

            self.df["Download_Method"]

            .fillna("Manual")

            .astype(str)

            .str.strip()

            .replace(METHOD_MAP)

        )

    def normalize_automation(self):

        self.df["Automation"] = (

            self.df["Automation"]

            .fillna("Manual")

            .astype(str)

            .str.strip()

            .replace(AUTO_MAP)

        )

    def save(self):

        OUTPUT.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        self.df.to_csv(

            OUTPUT,

            index=False

        )

    def run(self):

        print("=" * 70)
        print("GOHIF REGISTRY NORMALIZER")
        print("=" * 70)
        print()

        self.normalize_download_method()

        self.normalize_automation()

        self.save()

        print("Download Method Summary")
        print("-----------------------")
        print(self.df["Download_Method"].value_counts())

        print()

        print("Automation Summary")
        print("------------------")
        print(self.df["Automation"].value_counts())

        print()

        print(f"Normalized registry written to:\n{OUTPUT}")
if __name__ == "__main__":

    normalizer = RegistryNormalizer()

    normalizer.run()
