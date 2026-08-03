from pathlib import Path
import subprocess


pdb_dir = Path(
"analysis/structure_discovery/acquisition/pdb_files"
)

out_dir = Path(
"analysis/structure_discovery/docking/receptors/pdbqt"
)

out_dir.mkdir(parents=True, exist_ok=True)


for pdb in pdb_dir.glob("*.pdb"):

    output = out_dir / (
        pdb.stem + ".pdbqt"
    )

    cmd = [

        "obabel",

        str(pdb),

        "-O",

        str(output),

        "-xr"

    ]


    try:

        subprocess.run(
            cmd,
            check=True
        )

        print(
        f"Prepared: {output}"
        )

    except Exception as e:

        print(
        f"Failed {pdb}: {e}"
        )


print("="*80)
print("GOHIF RECEPTOR PREPARATION COMPLETE")
print("="*80)

