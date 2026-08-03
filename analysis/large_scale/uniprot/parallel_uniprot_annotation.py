import concurrent.futures
import requests
import pandas as pd
from pathlib import Path

INPUT="analysis/large_scale/uniprot/unique_gene_queries.csv"
OUTPUT="analysis/large_scale/uniprot/uniprot_annotations_parallel.csv"

queries=pd.read_csv(INPUT)

cache={}

if Path(OUTPUT).exists():
    old=pd.read_csv(OUTPUT)
    for _,r in old.iterrows():
        cache[r["query"]]=r.to_dict()

records=list(cache.values())

todo=[q for q in queries["query"] if q not in cache]

print("="*80)
print("GOHIF PARALLEL UNIPROT ENGINE")
print("="*80)
print("Cached:",len(cache))
print("Remaining:",len(todo))
print()

URL="https://rest.uniprot.org/uniprotkb/search"

session=requests.Session()

HEADERS={
"User-Agent":"GOHIF-Framework/1.0"
}

def annotate(gene):

    params={
        "query":f"gene:{gene}",
        "fields":"accession,gene_names,protein_name,organism_name",
        "format":"json",
        "size":1
    }

    try:

        r=session.get(
            URL,
            params=params,
            headers=HEADERS,
            timeout=20
        )

        if r.status_code!=200:
            return None

        j=r.json()

        if len(j.get("results",[]))==0:
            return None

        hit=j["results"][0]

        return{
            "query":gene,
            "accession":hit.get("primaryAccession",""),
            "entry":hit.get("uniProtkbId",""),
            "organism":hit.get("organism",{}).get("scientificName",""),
            "protein_name":str(hit.get("proteinDescription",""))
        }

    except Exception:
        return None


count=0

with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:

    futures=[executor.submit(annotate,g) for g in todo]

    for future in concurrent.futures.as_completed(futures):

        x=future.result()

        if x:
            records.append(x)

        count+=1

        if count%100==0:

            pd.DataFrame(records).drop_duplicates(
                subset="query"
            ).to_csv(
                OUTPUT,
                index=False
            )

            print(f"{count}/{len(todo)} processed")

pd.DataFrame(records).drop_duplicates(
subset="query"
).to_csv(
OUTPUT,
index=False
)

print()
print("="*80)
print("GOHIF PARALLEL ANNOTATION COMPLETE")
print("="*80)
print("Retrieved:",len(records))
