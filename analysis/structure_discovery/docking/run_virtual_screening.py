import pandas as pd
from pathlib import Path


ligands=pd.read_csv(
"analysis/structure_discovery/docking/ligands/ligand_library.csv"
)

targets=pd.read_csv(
"analysis/structure_discovery/docking/configs/receptor_config.csv"
)


results=[]


for _,t in targets.iterrows():

    for _,l in ligands.iterrows():

        results.append({

        "target_id":t.target_id,

        "ligand_id":l.ligand_id,

        "status":"waiting_for_ligand_structure",

        "binding_affinity":"NA"

        })


df=pd.DataFrame(results)


df.to_csv(
"analysis/structure_discovery/docking/results/virtual_screening_results.csv",
index=False
)


print("="*80)
print("GOHIF VIRTUAL SCREENING ENGINE INITIALIZED")
print("="*80)

print(df.to_string(index=False))


