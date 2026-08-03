from vina import Vina
import pandas as pd
from pathlib import Path


jobs = pd.read_csv(
"analysis/structure_discovery/docking/results/vina_screening_jobs.csv"
)


receptor_dir = Path(
"analysis/structure_discovery/docking/receptors/pdbqt"
)

ligand_dir = Path(
"analysis/structure_discovery/docking/ligand_library/pdbqt"
)

out_dir = Path(
"analysis/structure_discovery/docking/results/vina_outputs"
)

out_dir.mkdir(exist_ok=True)


results=[]


for _,job in jobs.iterrows():

    receptor = receptor_dir / job["receptor"]

    ligand = ligand_dir / (
        job["ligand_id"] + ".pdbqt"
    )


    try:

        v = Vina(
            sf_name="vina"
        )

        v.set_receptor(
            str(receptor)
        )

        v.set_ligand_from_file(
            str(ligand)
        )


        # temporary search box
        # replace later with active site coordinates

        v.compute_vina_maps(
            center=[10,-30,5],
            box_size=[30,30,30]
        )


        v.dock(
            exhaustiveness=8,
            n_poses=5
        )


        affinity = v.poses(
            n_poses=1
        )


        out_file = out_dir / (
        job["target_id"]+"_"+job["ligand_id"]+".pdbqt"
        )


        v.write_poses(
            str(out_file),
            n_poses=1,
            overwrite=True
        )


        status="completed"


    except Exception as e:

        affinity=str(e)
        status="failed"


    results.append({

        "target_id":job["target_id"],
        "ligand_id":job["ligand_id"],
        "compound":job["compound"],
        "status":status,
        "result":str(affinity)

    })


pd.DataFrame(results).to_csv(
"analysis/structure_discovery/docking/results/vina_execution_results.csv",
index=False
)


print("="*80)
print("GOHIF PYTHON VINA EXECUTION COMPLETE")
print("="*80)

