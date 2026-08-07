#!/usr/bin/env python3

from pathlib import Path
import subprocess

ROOT = Path.home() / "GOHIF"

SDF_DIR = ROOT / "analysis/structure_validation/ligands/sdf"

targets = [
"GOHIF-033",
"GOHIF-052",
"GOHIF-093",
"GOHIF-158",
"GOHIF-214",
"GOHIF-219",
"GOHIF-234",
"GOHIF-235",
"GOHIF-242",
"GOHIF-246",
]

print("="*80)
print("GOHIF")
print("Fix Remaining 2D Ligands")
print("="*80)

for ligand in targets:

    files = list(SDF_DIR.glob(f"{ligand}_*.sdf"))

    if not files:
        print(f"{ligand:<12} MISSING")
        continue

    sdf = files[0]

    try:

        subprocess.run(
            [
                "obabel",
                str(sdf),
                "-O",
                str(sdf),
                "--gen3d"
            ],
            check=True,
            timeout=300
        )

        print(f"{ligand:<12} SUCCESS")

    except subprocess.TimeoutExpired:

        print(f"{ligand:<12} TIMEOUT")

    except Exception as e:

        print(f"{ligand:<12} FAILED")
        print(e)

print("="*80)
