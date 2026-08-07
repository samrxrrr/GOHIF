#!/usr/bin/env python3

from pathlib import Path
import subprocess
import pandas as pd

ROOT = Path.home() / "GOHIF"

SDF_DIR = ROOT / "analysis/structure_validation/ligands/sdf"
PDBQT_DIR = ROOT / "analysis/structure_validation/ligands/pdbqt"
REPORT_DIR = ROOT / "analysis/structure_validation/ligands/reports"
LOG_DIR = ROOT / "analysis/structure_validation/ligands/logs"

PDBQT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

REPORT = REPORT_DIR / "Ligand_PDBQT_Report.csv"

print("="*80)
print("GOHIF Phase II")
print("Ligand PDBQT Preparation")
print("="*80)
print()

results = []

success = 0
failed = 0

sdf_files = sorted(SDF_DIR.glob("GOHIF-*.sdf"))

print("Ligands :", len(sdf_files))
print()

for sdf in sdf_files:

    ligand = sdf.stem

    pdbqt = PDBQT_DIR / f"{ligand}.pdbqt"

    log = LOG_DIR / f"{ligand}.log"

    cmd = [
        "mk_prepare_ligand.py",
        "-i", str(sdf),
        "-o", str(pdbqt)
    ]

    try:

        with open(log, "w") as logfile:

            subprocess.run(
                cmd,
                stdout=logfile,
                stderr=subprocess.STDOUT,
                check=True,
                timeout=180
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

    print(f"{ligand:<20} {status}")

report = pd.DataFrame(results)

report.to_csv(REPORT, index=False)

print()

print("="*80)
print("SUMMARY")
print("="*80)

print("Success :", success)
print("Failed  :", failed)

print()
print("Report :", REPORT)
print("PDBQT  :", PDBQT_DIR)
print("Logs   :", LOG_DIR)
