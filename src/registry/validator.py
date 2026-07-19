from pathlib import Path
import pandas as pd

from src.registry.loader import RegistryLoader


class RegistryValidator:

    OUTPUT = Path("metadata/registry/GOHIF_VALIDATION_REPORT.csv")

    REQUIRED = [
        "GOHIF_ID",
        "Dataset_Name",
        "Organization",
        "One_Health_Domain",
    ]

    WARNING = [
        "Official_Website",
        "Download_URL",
        "License",
    ]

    def __init__(self):
        self.loader = RegistryLoader()

    def validate(self):

        df = self.loader.load()

        issues = []

        # Required fields (ERROR)
        for col in self.REQUIRED:

            if col not in df.columns:
                issues.append({
                    "Severity":"ERROR",
                    "Issue":"Missing Column",
                    "Column":col,
                    "GOHIF_ID":"",
                    "Dataset_Name":""
                })
                continue

            missing = df[df[col].fillna("").astype(str).str.strip()==""]

            for _,row in missing.iterrows():
                issues.append({
                    "Severity":"ERROR",
                    "Issue":"Missing Value",
                    "Column":col,
                    "GOHIF_ID":row["GOHIF_ID"],
                    "Dataset_Name":row["Dataset_Name"]
                })

        # Advisory fields (WARNING)
        for col in self.WARNING:

            if col not in df.columns:
                continue

            missing = df[df[col].fillna("").astype(str).str.strip()==""]

            for _,row in missing.iterrows():
                issues.append({
                    "Severity":"WARNING",
                    "Issue":"Missing Value",
                    "Column":col,
                    "GOHIF_ID":row["GOHIF_ID"],
                    "Dataset_Name":row["Dataset_Name"]
                })

        # Duplicate IDs (ERROR)
        dup = df[df.duplicated("GOHIF_ID", keep=False)]

        for _,row in dup.iterrows():
            issues.append({
                "Severity":"ERROR",
                "Issue":"Duplicate GOHIF_ID",
                "Column":"GOHIF_ID",
                "GOHIF_ID":row["GOHIF_ID"],
                "Dataset_Name":row["Dataset_Name"]
            })

        report = pd.DataFrame(issues)

        self.OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        report.to_csv(self.OUTPUT,index=False)

        return report


if __name__ == "__main__":

    report = RegistryValidator().validate()

    print(report.groupby("Severity").size())
