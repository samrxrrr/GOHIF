from pathlib import Path
import pandas as pd
import subprocess


dock_dir = Path(
"analysis/structure_discovery/docking/results/vina_outputs"
)

out_dir = Path(
"analysis/drug_discovery/interactions/plip_results"
)

out_dir.mkdir(exist_ok=True)


results=[]


for pose in dock_dir.glob("*.pdbqt"):

    complex_file = out_dir / (
        pose.stem + ".pdb"
    )


    # Convert pdbqt to pdb
    subprocess.run(
        [
        "obabel",
        "-ipdbqt",
        str(pose),
        "-opdb",
        "-O",
        str(complex_file)
        ],
        capture_output=True
    )


    plip_output = out_dir / (
        pose.stem + "_plip.xml"
    )


    try:

        subprocess.run(
        [
        "plip",
        "-f",
        str(complex_file),
        "-x",
        "-o",
        str(out_dir)
        ],
        check=True
        )


        status="completed"


    except Exception as e:

        status="failed"


    results.append({

        "complex":pose.stem,
        "status":status

    })


pd.DataFrame(results).to_csv(
"analysis/drug_discovery/interactions/plip_results/plip_status.csv",
index=False
)


print("="*80)
print("GOHIF PLIP INTERACTION ANALYSIS COMPLETE")
print("="*80)

print(
pd.DataFrame(results).to_string(index=False)
)

