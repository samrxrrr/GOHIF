#!/usr/bin/env python3

from pathlib import Path
import subprocess
import pandas as pd

ROOT = Path.home() / "GOHIF"

SDF_DIR = ROOT / "analysis/structure_validation/ligands/sdf"
PDB_DIR = ROOT / "analysis/structure_validation/ligands/pdb"
REPORT_DIR = ROOT / "analysis/structure_validation/ligands/reports"

PDB_DIR.mkdir(parents=True, exist_ok=True)

REPORT = REPORT_DIR / "SDF_to_PDB_Report.csv"

print("="*80)
print("GOHIF Phase II")
print("SDF → PDB Conversion")
print("="*80)
print()

results = []

success = 0
failed = 0

exclude = {
    "GOHIF-033",
}

for sdf in sorted(SDF_DIR.glob("GOHIF-*.sdf")):

    ligand = sdf.stem.split("_")[0]

    if ligand in exclude:

        print(f"{ligand:<12} SKIPPED")

        results.append({
            "LigandID": ligand,
            "Status": "SKIPPED"
        })

        continue

    pdb = PDB_DIR / (sdf.stem + ".pdb")

    cmd = [
        "obabel",
        str(sdf),
        "-O",
        str(pdb)
    ]

    try:

        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        status = "SUCCESS"
        success += 1

    except Exception:

        status = "FAILED"
        failed += 1

    results.append({
        "LigandID": ligand,
        "Status": status
    })

    print(f"{ligand:<12} {status}")

report = pd.DataFrame(results)

report.to_csv(REPORT, index=False)

print()

print("="*80)
print("SUMMARY")
print("="*80)

print("Success :", success)
print("Failed  :", failed)
print("Skipped :", len(exclude))

print()
print(REPORT)
