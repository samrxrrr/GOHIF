#!/usr/bin/env python3

from pathlib import Path
import subprocess

ROOT = Path.home() / "GOHIF"

SDF_DIR = ROOT / "analysis/structure_validation/ligands/sdf"
PDBQT_DIR = ROOT / "analysis/structure_validation/ligands/pdbqt"
LOG_DIR = ROOT / "analysis/structure_validation/ligands/logs"

failed = [
"GOHIF-029",
"GOHIF-050",
"GOHIF-052",
"GOHIF-060",
"GOHIF-061",
"GOHIF-062",
"GOHIF-063",
"GOHIF-079",
"GOHIF-080",
"GOHIF-089",
"GOHIF-097",
"GOHIF-146",
"GOHIF-194",
"GOHIF-207",
"GOHIF-247",
"GOHIF-250"
]

print("="*80)
print("Retry PDBQT Generation")
print("="*80)

success = 0
failed_count = 0

for lig in failed:

    sdf = list(SDF_DIR.glob(f"{lig}_*.sdf"))[0]

    pdbqt = PDBQT_DIR / f"{sdf.stem}.pdbqt"

    log = LOG_DIR / f"{sdf.stem}.retry.log"

    cmd = [
        "mk_prepare_ligand.py",
        "-i", str(sdf),
        "-o", str(pdbqt)
    ]

    try:
        with open(log, "w") as f:
            subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.STDOUT,
                check=True
            )

        print(f"{lig:<12} SUCCESS")
        success += 1

    except Exception:
        print(f"{lig:<12} FAILED")
        failed_count += 1

print()
print("="*80)
print("Recovered :", success)
print("Still failed :", failed_count)
print("="*80)
