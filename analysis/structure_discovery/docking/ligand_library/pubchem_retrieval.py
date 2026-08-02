import pandas as pd
import requests
from pathlib import Path


input_file = (
"analysis/structure_discovery/docking/"
"ligand_library/ligand_candidates.csv"
)


sdf_dir = Path(
"analysis/structure_discovery/docking/"
"ligand_library/sdf"
)

sdf_dir.mkdir(exist_ok=True)


df = pd.read_csv(input_file)


results=[]


for _,row in df.iterrows():

    name=row["compound_name"]

    try:

        cid_url = (
        f"https://pubchem.ncbi.nlm.nih.gov/"
        f"rest/pug/compound/name/{name}/cids/JSON"
        )

        cid_data=requests.get(
            cid_url,
            timeout=20
        ).json()


        cid=cid_data["IdentifierList"]["CID"][0]


        sdf_url=(
        f"https://pubchem.ncbi.nlm.nih.gov/"
        f"rest/pug/compound/cid/{cid}/SDF"
        )


        sdf=requests.get(
            sdf_url,
            timeout=30
        ).text


        sdf_file=sdf_dir/f"{row['ligand_id']}.sdf"


        sdf_file.write_text(
            sdf
        )


        results.append({

        "ligand_id":row["ligand_id"],

        "compound_name":name,

        "cid":cid,

        "sdf_file":str(sdf_file),

        "status":"downloaded"

        })


    except Exception as e:


        results.append({

        "ligand_id":row["ligand_id"],

        "compound_name":name,

        "cid":"NA",

        "sdf_file":"NA",

        "status":str(e)

        })


out=pd.DataFrame(results)


out.to_csv(
"analysis/structure_discovery/docking/"
"ligand_library/pubchem_results.csv",
index=False
)


print("="*80)
print("GOHIF PUBCHEM LIGAND RETRIEVAL COMPLETE")
print("="*80)

print(out.to_string(index=False))

