import pandas as pd


tracker=pd.read_csv(
"analysis/structure_discovery/acquisition/structure_acquisition_tracker.csv"
)


results=[]


for _,row in tracker.iterrows():

    results.append({

        "target_id":row["target_id"],

        "protein":row["protein"],

        "pathogen":row["pathogen"],

        "uniprot_id":"PENDING",

        "pdb_id":"PENDING",

        "mapping_status":"awaiting_identifier"

    })


out=pd.DataFrame(results)


out.to_csv(
"analysis/structure_discovery/acquisition/uniprot_pdb_mapping_results.csv",
index=False
)


print("="*80)
print("GOHIF UNIPROT-PDB MAPPING ENGINE COMPLETE")
print("="*80)

print(out.to_string(index=False))

print("\nSaved:")
print(
"analysis/structure_discovery/acquisition/uniprot_pdb_mapping_results.csv"
)

