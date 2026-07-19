from pathlib import Path
import pandas as pd

from src.registry.loader import RegistryLoader


class AliasManager:

    OUTPUT = Path("metadata/registry/GOHIF_ALIAS_REPORT.csv")

    def __init__(self):
        self.loader = RegistryLoader()

    def build(self):

        df = self.loader.load()

        rows = []

        for name, group in df.groupby("Dataset_Name"):

            if len(group) < 2:
                continue

            domains = sorted(group["One_Health_Domain"].dropna().unique())

            if len(domains) > 1:
                status = "MULTI_DOMAIN_RESOURCE"
            else:
                status = "POSSIBLE_DUPLICATE"

            rows.append({
                "Dataset_Name": name,
                "Occurrences": len(group),
                "Domains": "; ".join(domains),
                "Classification": status,
                "GOHIF_IDs": "; ".join(group["GOHIF_ID"].astype(str))
            })

        report = pd.DataFrame(rows).sort_values(
            ["Classification", "Dataset_Name"]
        )

        self.OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        report.to_csv(self.OUTPUT, index=False)

        return report


if __name__ == "__main__":

    report = AliasManager().build()

    print()
    print(report)
