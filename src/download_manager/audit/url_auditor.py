from pathlib import Path
from datetime import datetime
import requests
import pandas as pd


REGISTRY = Path(
    "metadata/registry/GOHIF_MASTER_DATASET_REGISTRY.csv"
)

REPORT = Path(
    "reports/url_audit/URL_AUDIT_REPORT.csv"
)


class URLAuditor:

    def __init__(self):

        self.timeout = 30

        self.session = requests.Session()

        self.session.headers.update({

            "User-Agent":
            "GOHIF/1.0"

        })

    def classify(self, url):

        if pd.isna(url):

            return "EMPTY", ""

        url = str(url).strip()

        if url == "":

            return "EMPTY", ""

        try:

            r = self.session.head(

                url,

                timeout=self.timeout,

                allow_redirects=True

            )

            return (

                str(r.status_code),

                r.url

            )

        except requests.exceptions.SSLError:

            return (

                "SSL_ERROR",

                url

            )

        except requests.exceptions.Timeout:

            return (

                "TIMEOUT",

                url

            )

        except requests.exceptions.ConnectionError:

            return (

                "CONNECTION_ERROR",

                url

            )

        except Exception:

            return (

                "UNKNOWN",

                url

            )
    def run(self):

        df = pd.read_csv(REGISTRY)

        results = []

        total = len(df)

        print("=" * 70)
        print("GOHIF URL AUDITOR")
        print("=" * 70)
        print()

        for i, (_, row) in enumerate(df.iterrows(), start=1):

            status, final_url = self.classify(

                row.get("Download_URL", "")

            )

            print(

                f"[{i:03d}/{total}] "

                f"{row['GOHIF_ID']} "

                f"{status}"

            )

            results.append({

                "GOHIF_ID":

                    row["GOHIF_ID"],

                "Dataset_Name":

                    row["Dataset_Name"],

                "Download_URL":

                    row.get("Download_URL", ""),

                "URL_Status":

                    status,

                "Resolved_URL":

                    final_url,

                "Audit_Time":

                    datetime.now().isoformat(
                        timespec="seconds"
                    )

            })

        report = pd.DataFrame(results)

        REPORT.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        report.to_csv(

            REPORT,

            index=False

        )

        print()

        print("=" * 70)

        print("Audit Finished")

        print("=" * 70)

        print()

        print(report["URL_Status"].value_counts())

        print()

        print(f"Saved to: {REPORT}")
if __name__ == "__main__":

    auditor = URLAuditor()

    auditor.run()
