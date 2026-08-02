import requests
import pandas as pd
from pathlib import Path


input_file = (
"analysis/structure_discovery/acquisition/"
"structure_acquisition_tracker.csv"
)

out_dir = Path(
"analysis/structure_discovery/acquisition/pdb_files"
)

out_dir.mkdir(exist_ok=True)


targets = pd.read_csv(input_file)


results=[]


def search_pdb(protein):

    url="https://search.rcsb.org/rcsbsearch/v2/query"

    query={
    "query":{
        "type":"terminal",
        "service":"full_text",
        "parameters":{
            "value":protein
        }
    },
    "return_type":"entry"
    }

    try:
        r=requests.post(
            url,
            json=query,
            timeout=20
        )

        data=r.json()

        ids=[]

        for x in data.get("result_set",[])[:5]:
            ids.append(
                x["identifier"]
            )

        return ids

    except Exception:
        return []


def download_pdb(pdb_id):

    url=(
    f"https://files.rcsb.org/download/{pdb_id}.pdb"
    )

    path=out_dir/f"{pdb_id}.pdb"

    try:

        r=requests.get(
            url,
            timeout=30
        )

        if r.status_code==200:

            path.write_text(
                r.text
            )

            return str(path)

    except Exception:
        pass


    return "FAILED"



for _,row in targets.iterrows():

    pdbs=search_pdb(
        row["protein"]
    )

    selected="NA"
    file="NA"

    if pdbs:

        selected=pdbs[0]

        file=download_pdb(
            selected
        )


    results.append({

    "target_id":row["target_id"],

    "protein":row["protein"],

    "pathogen":row["pathogen"],

    "pdb_id":selected,

    "pdb_file":file

    })


out=pd.DataFrame(results)


out.to_csv(
"analysis/structure_discovery/acquisition/"
"auto_structure_results.csv",
index=False
)


print("="*80)
print("GOHIF AUTOMATIC STRUCTURE DOWNLOAD COMPLETE")
print("="*80)

print(out.to_string(index=False))

