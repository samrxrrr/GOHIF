from pathlib import Path
import pandas as pd

from src.registry.loader import RegistryLoader


class FAIRScorer:

    OUTPUT = Path("metadata/registry/GOHIF_FAIR_SCORES.csv")

    def __init__(self):
        self.loader = RegistryLoader()

    @staticmethod
    def has_value(v):
        return pd.notna(v) and str(v).strip() != ""

    def score(self):

        df = self.loader.load()
        results = []

        for _, row in df.iterrows():

            # ---------- Findable (25) ----------
            f = 0
            if self.has_value(row.get("GOHIF_ID")):
                f += 10
            if self.has_value(row.get("Dataset_Name")):
                f += 5
            if self.has_value(row.get("Organization")):
                f += 5
            if self.has_value(row.get("Keywords")):
                f += 5

            # ---------- Accessible (25) ----------
            a = 0
            if self.has_value(row.get("Official_Website")):
                a += 10
            if self.has_value(row.get("Download_URL")):
                a += 10
            if self.has_value(row.get("Access_Type")):
                a += 5

            # ---------- Interoperable (25) ----------
            i = 0
            if self.has_value(row.get("Data_Format")):
                i += 10
            if self.has_value(row.get("API_Available")):
                i += 10
            if self.has_value(row.get("Version")):
                i += 5

            # ---------- Reusable (25) ----------
            r = 0
            if self.has_value(row.get("License")):
                r += 10
            if self.has_value(row.get("Update_Frequency")):
                r += 10
            if self.has_value(row.get("Citation")):
                r += 5

            total = f + a + i + r

            results.append({
                "GOHIF_ID": row["GOHIF_ID"],
                "Dataset_Name": row["Dataset_Name"],
                "Findable": f,
                "Accessible": a,
                "Interoperable": i,
                "Reusable": r,
                "FAIR_Score": total
            })

        out = pd.DataFrame(results)
        out.to_csv(self.OUTPUT, index=False)
        return out


if __name__ == "__main__":
    print(FAIRScorer().score().head())
