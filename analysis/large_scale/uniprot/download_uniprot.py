import pandas as pd
import requests
import time

queries=pd.read_csv(
"analysis/large_scale/uniprot/uniprot_queries.csv"
)

records=[]

for i,row in queries.iterrows():

    gene=row["gene"]

    url=(
        "https://rest.uniprot.org/uniprotkb/search"
        f"?query=gene:{gene}"
        "&fields="
        "accession,"
        "gene_names,"
        "protein_name,"
        "organism_name,"
        "go_id,"
        "keyword,"
        "cc_function"
        "&format=json"
        "&size=1"
    )

    try:

        r=requests.get(url,timeout=30)

        data=r.json()

        if data.get("results"):

            hit=data["results"][0]

            records.append({

                "gene":gene,

                "accession":
                hit.get("primaryAccession",""),

                "entry":
                hit.get("uniProtkbId",""),

                "protein_name":
                str(hit.get("proteinDescription","")),

                "organism":
                hit.get("organism",{}).get("scientificName",""),

                "go_terms":
                str(hit.get("uniProtKBCrossReferences","")),

                "keywords":
                str(hit.get("keywords",""))

            })

    except Exception:

        pass

    if i%100==0:

        print(i,"/",len(queries))

    time.sleep(0.1)

pd.DataFrame(records).to_csv(
"analysis/large_scale/uniprot/uniprot_annotations.csv",
index=False
)

print("="*80)
print("GOHIF UNIPROT DOWNLOAD COMPLETE")
print("="*80)
print("Retrieved:",len(records))
