from pathlib import Path
import subprocess


sdf_dir = Path(
"analysis/structure_discovery/docking/ligand_library/sdf"
)

pdbqt_dir = Path(
"analysis/structure_discovery/docking/ligand_library/pdbqt"
)

pdbqt_dir.mkdir(exist_ok=True)


for sdf in sdf_dir.glob("*.sdf"):

    output = pdbqt_dir / (
        sdf.stem + ".pdbqt"
    )

    cmd = [
        "obabel",
        str(sdf),
        "-O",
        str(output),
        "--gen3d",
        "-h"
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
            f"Failed {sdf}: {e}"
        )


print("="*80)
print("GOHIF LIGAND PREPARATION COMPLETE")
print("="*80)

