import pandas as pd
import requests
import time

queries=pd.read_csv(
"analysis/biological_annotation/uniprot_queries.csv"
)

records=[]

for _,r in queries.iterrows():

    q=r["uniprot_query"]

    url=(
    "https://rest.uniprot.org/uniprotkb/search"
    f"?query={q}&format=json&size=1"
    )

    try:

        x=requests.get(url,timeout=30).json()

        if x.get("results"):

            hit=x["results"][0]

            records.append({

            "protein":r["protein"],
            "pathogen":r["pathogen"],
            "accession":hit.get("primaryAccession",""),
            "entry":hit.get("uniProtkbId",""),
            "protein_name":
            hit.get("proteinDescription",{}),

            })

        else:

            records.append({

            "protein":r["protein"],
            "pathogen":r["pathogen"],
            "accession":"",
            "entry":"",
            "protein_name":""

            })

    except:

        records.append({

        "protein":r["protein"],
        "pathogen":r["pathogen"],
        "accession":"",
        "entry":"",
        "protein_name":""

        })

    time.sleep(1)

pd.DataFrame(records).to_csv(
"analysis/biological_annotation/uniprot_hits.csv",
index=False
)

print("="*80)
print("GOHIF UNIPROT RETRIEVAL COMPLETE")
print("="*80)
print(pd.DataFrame(records).to_string(index=False))
