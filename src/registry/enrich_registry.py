from pathlib import Path
import pandas as pd

REGISTRY = Path(
    "metadata/registry/GOHIF_MASTER_DATASET_REGISTRY.csv"
)

OUTPUT = Path(
    "metadata/registry/GOHIF_MASTER_DATASET_REGISTRY_ENRICHED.csv"
)

REPORT = Path(
    "reports/registry/registry_enrichment_report.csv"
)


class RegistryEnricher:

    def __init__(self):

        self.df = pd.read_csv(REGISTRY)

    def fill_download_fields(self):

        for idx, row in self.df.iterrows():

            method = row.get("Download_Method")

            if pd.notna(method):
                continue

            url = row.get("Download_URL")
            api = row.get("API_Base")
            ftp = row.get("FTP_Path")
            git = row.get("Git_Repo")
            cli = row.get("CLI_Command")

            if pd.notna(api):
                self.df.at[idx, "Download_Method"] = "API"
                self.df.at[idx, "Automation"] = "Automatic"

            elif pd.notna(ftp):
                self.df.at[idx, "Download_Method"] = "FTP"
                self.df.at[idx, "Automation"] = "Automatic"

            elif pd.notna(git):
                self.df.at[idx, "Download_Method"] = "Git"
                self.df.at[idx, "Automation"] = "Automatic"

            elif pd.notna(cli):
                self.df.at[idx, "Download_Method"] = "CLI"
                self.df.at[idx, "Automation"] = "Automatic"

            elif pd.notna(url):
                self.df.at[idx, "Download_Method"] = "HTTP"
                self.df.at[idx, "Automation"] = "Automatic"

            else:
                self.df.at[idx, "Download_Method"] = "Manual"
                self.df.at[idx, "Automation"] = "Manual"
    def generate_report(self):

        report = pd.DataFrame({

            "Download_Method":
                self.df["Download_Method"],

            "Automation":
                self.df["Automation"]

        })

        report = (

            report

            .value_counts()

            .reset_index(name="Count")

            .sort_values(

                "Count",

                ascending=False

            )

        )

        REPORT.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        report.to_csv(

            REPORT,

            index=False

        )

        return report

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
        print("GOHIF REGISTRY ENRICHMENT")
        print("=" * 70)
        print()

        before = self.df["Download_Method"].isna().sum()

        self.fill_download_fields()

        after = self.df["Download_Method"].isna().sum()

        report = self.generate_report()

        self.save()

        print(f"Missing Download_Method before : {before}")
        print(f"Missing Download_Method after  : {after}")
        print()

        print(report)

        print()

        print(f"Enriched registry written to:\n{OUTPUT}")
        print(f"Summary report written to:\n{REPORT}")

if __name__ == "__main__":

    enricher = RegistryEnricher()

    enricher.run()
