#!/usr/bin/env python3

"""
GOHIF Phase II
Generate 3D coordinates for recovered PubChem 2D SDF files
"""

from pathlib import Path
import subprocess
import pandas as pd

ROOT = Path.home() / "GOHIF"

SDF_DIR = ROOT / "analysis/structure_validation/ligands/sdf"

REPORT_DIR = ROOT / "analysis/structure_validation/ligands/reports"

RETRY_REPORT = REPORT_DIR / "PubChem_2D_Retry_Report.csv"

REPORT = REPORT_DIR / "Generate3D_Report.csv"

df = pd.read_csv(RETRY_REPORT)

print("="*80)
print("GOHIF")
print("Generate 3D Coordinates")
print("="*80)
print()

results = []

success = 0
failed = 0

recover = df[df["Status"] == "SUCCESS"]

print(f"Recovered 2D ligands : {len(recover)}")
print()

for _, row in recover.iterrows():

    ligand = row["LigandID"]
    cid = int(row["PubChemCID"])

    # Skip problematic ligand
    if ligand == "GOHIF-214":
        print(f"{ligand:<12} SKIPPED")
        results.append({
            "LigandID": ligand,
            "PubChemCID": cid,
            "Status": "SKIPPED"
        })
        continue

    sdf = SDF_DIR / f"{ligand}_{cid}.sdf"

    # Skip already processed files
    if sdf.exists() and sdf.stat().st_size > 5000:
        print(f"{ligand:<12} ALREADY_DONE")
        results.append({
            "LigandID": ligand,
            "PubChemCID": cid,
            "Status": "ALREADY_DONE"
        })
        continue

    cmd = [
        "obabel",
        str(sdf),
        "-O",
        str(sdf),
        "--gen3d"
    ]

    try:

        subprocess.run(
            cmd,
            check=True,
            timeout=180,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        status = "SUCCESS"
        success += 1

    except subprocess.TimeoutExpired:

        status = "TIMEOUT"
        failed += 1

    except Exception:

        status = "FAILED"
        failed += 1

    results.append({
        "LigandID": ligand,
        "PubChemCID": cid,
        "Status": status
    })

    print(f"{ligand:<12} {status}")
report = pd.DataFrame(results)

report.to_csv(REPORT, index=False)

print()

print("="*80)
print("SUMMARY")
print("="*80)

print("3D Generated :", success)
print("Failed :", failed)

print()

print(REPORT)
