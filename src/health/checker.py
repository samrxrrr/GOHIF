from pathlib import Path
import pandas as pd

from src.registry.loader import RegistryLoader


class HealthChecker:

    OUTPUT = Path("metadata/registry/GOHIF_HEALTH_REPORT.csv")

    def __init__(self):
        self.loader = RegistryLoader()

    @staticmethod
    def ok(v):
        return pd.notna(v) and str(v).strip() != ""

    def evaluate(self):

        df = self.loader.load()
        rows = []

        for _, r in df.iterrows():

            score = 0

            # Connectivity (30)
            if self.ok(r.get("Download_URL")):
                score += 10
            if self.ok(r.get("API_Base")):
                score += 10
            if self.ok(r.get("FTP_Path")):
                score += 10

            # Automation (20)
            if self.ok(r.get("Automation")):
                score += 10
            if self.ok(r.get("Download_Method")):
                score += 10

            # Integrity (20)
            if self.ok(r.get("Checksum")):
                score += 10
            if self.ok(r.get("SHA256")):
                score += 10

            # Local availability (20)
            if self.ok(r.get("Local_File")):
                score += 10
            if str(r.get("Downloaded","")).strip().lower() in ("yes","true"):
                score += 10

            # Registry status (10)
            if str(r.get("Download_Status","")).strip().lower() in (
                "completed",
                "downloaded",
                "available",
                "success"
            ):
                score += 10

            if score >= 90:
                status = "EXCELLENT"
            elif score >= 70:
                status = "GOOD"
            elif score >= 50:
                status = "FAIR"
            elif score >= 30:
                status = "LIMITED"
            else:
                status = "NOT_READY"

            rows.append({
                "GOHIF_ID": r["GOHIF_ID"],
                "Dataset_Name": r["Dataset_Name"],
                "Health_Score": score,
                "Health_Status": status
            })

        out = pd.DataFrame(rows)
        out.to_csv(self.OUTPUT, index=False)

        return out


if __name__ == "__main__":
    print(HealthChecker().evaluate().head())
