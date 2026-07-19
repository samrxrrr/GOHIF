from pathlib import Path
import pandas as pd

from src.registry.loader import RegistryLoader
from src.download_manager.adapter_resolver import AdapterResolver


OUTPUT = Path("metadata/registry/GOHIF_DOWNLOAD_QUEUE.csv")


def main():

    df = RegistryLoader().load()

    queue = []

    for _, row in df.iterrows():

        url = str(row.get("Download_URL","")).strip()

        if not url:
            continue

        queue.append({

            "GOHIF_ID": row["GOHIF_ID"],

            "Dataset_Name": row["Dataset_Name"],

            "Adapter": AdapterResolver.resolve(row),

            "Download_URL": url,

            "Download_Status": row.get("Download_Status",""),

            "Downloaded": row.get("Downloaded","")

        })

    out = pd.DataFrame(queue)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUTPUT,index=False)

    print()

    print("Queue created")

    print("Datasets :",len(out))

    print()

    print(out["Adapter"].value_counts())


if __name__=="__main__":
    main()
