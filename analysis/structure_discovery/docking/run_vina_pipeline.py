import pandas as pd
from pathlib import Path
import subprocess


jobs=pd.read_csv(
"analysis/structure_discovery/docking/docking_jobs.csv"
)


results=[]


for _,row in jobs.iterrows():

    receptor=row["pdb_file"]
    ligand=row["ligand_file"]

    status="pending"

    if (
        str(receptor)!="NA"
        and
        str(ligand)!="NA"
    ):

        status="ready"

        # Future AutoDock Vina command
        #
        # vina \
        # --receptor receptor.pdbqt \
        # --ligand ligand.pdbqt \
        # --center_x ...
        #
    else:

        status="missing_structure_or_ligand"


    results.append({

        "target_id":row["target_id"],

        "protein":row["protein"],

        "pathogen":row["pathogen"],

        "vina_status":status

    })


out=pd.DataFrame(results)


out.to_csv(
"analysis/structure_discovery/docking/vina_pipeline_status.csv",
index=False
)


print("="*80)
print("GOHIF VINA PIPELINE CHECK COMPLETE")
print("="*80)

print(out.to_string(index=False))

print("\nSaved:")
print(
"analysis/structure_discovery/docking/vina_pipeline_status.csv"
)

