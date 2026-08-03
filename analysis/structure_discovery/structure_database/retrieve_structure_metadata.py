import pandas as pd
from pathlib import Path


query_file = (
"analysis/structure_discovery/structure_database/"
"structure_queries.csv"
)


df = pd.read_csv(query_file)


results=[]


for _, row in df.iterrows():

    results.append({

        "target_id": row["target_id"],

        "protein": row["protein"],

        "pathogen": row["pathogen"],

        "uniprot_id": row["uniprot_id"],

        "pdb_id": row["pdb_id"],

        "structure_status":
        "awaiting_database_mapping"

    })


out=pd.DataFrame(results)


out.to_csv(
"analysis/structure_discovery/structure_database/structure_metadata_results.csv",
index=False
)


print("="*80)
print("GOHIF STRUCTURE METADATA RETRIEVAL INTERFACE READY")
print("="*80)

print(out.to_string(index=False))

print("\nSaved:")
print(
"analysis/structure_discovery/structure_database/"
"structure_metadata_results.csv"
)

