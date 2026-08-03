import pandas as pd
import requests
import time

INPUT="analysis/large_scale/qc/high_confidence_amr_proteins.csv"
OUTPUT="analysis/large_scale/pdb/pdb_mapping.csv"

df=pd.read_csv(INPUT)

records=[]

for i,row in df.iterrows():

    accession=str(row["accession"])

    url=f"https://rest.uniprot.org/uniprotkb/{accession}.json"

    pdb_ids=[]

    try:

        r=requests.get(url,timeout=30)

        if r.status_code==200:

            j=r.json()

            refs=j.get("uniProtKBCrossReferences",[])

            for ref in refs:

                if ref.get("database")=="PDB":

                    pdb_ids.append(ref.get("id"))

    except:
        pass

    records.append({

        "normalized_gene":row["normalized_gene"],

        "accession":accession,

        "pdb_ids":";".join(sorted(set(pdb_ids))),

        "pdb_count":len(set(pdb_ids))

    })

    if (i+1)%100==0:

        print(f"{i+1}/{len(df)} processed")

        pd.DataFrame(records).to_csv(
            OUTPUT,
            index=False
        )

        time.sleep(0.2)

pd.DataFrame(records).to_csv(
OUTPUT,
index=False
)

print("="*80)
print("GOHIF PDB MAPPING COMPLETE")
print("="*80)

result=pd.DataFrame(records)

print("Proteins:",len(result))
print("Proteins with PDB:",
(result["pdb_count"]>0).sum())

print()

print(
result.sort_values(
"pdb_count",
ascending=False
).head(20).to_string(index=False)
)
