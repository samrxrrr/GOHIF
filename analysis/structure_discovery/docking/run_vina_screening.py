import pandas as pd
from pathlib import Path


targets=pd.read_csv(
"analysis/structure_discovery/docking/vina_configs/docking_config.csv"
)

ligands=pd.read_csv(
"analysis/structure_discovery/docking/ligand_library/ligand_library_final.csv"
)


results=[]


for _,t in targets.iterrows():

    for _,l in ligands.iterrows():

        results.append({

        "target_id":t.target_id,

        "receptor":t.receptor,

        "ligand_id":l.ligand_id,

        "compound":l.compound_name,

        "vina_status":"ready",

        "binding_affinity":"pending"

        })


df=pd.DataFrame(results)


df.to_csv(
"analysis/structure_discovery/docking/results/vina_screening_jobs.csv",
index=False
)


print("="*80)
print("GOHIF VINA SCREENING JOB MATRIX CREATED")
print("="*80)

print(df.head(15).to_string(index=False))

print("\nTotal docking jobs:",len(df))

