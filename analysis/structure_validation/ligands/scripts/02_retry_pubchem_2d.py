#!/usr/bin/env python3

"""
GOHIF Phase II
Retry PubChem downloads using 2D SDF
"""

from pathlib import Path
import pandas as pd
import requests
import time

ROOT = Path.home() / "GOHIF"

FAILED = ROOT / "analysis/structure_validation/ligands/reports/Failed_Downloads.csv"

SDF_DIR = ROOT / "analysis/structure_validation/ligands/sdf"

REPORT_DIR = ROOT / "analysis/structure_validation/ligands/reports"

REPORT = REPORT_DIR / "PubChem_2D_Retry_Report.csv"

df = pd.read_csv(FAILED)

print("="*80)
print("GOHIF")
print("PubChem 2D Retry")
print("="*80)
print(f"Failed ligands : {len(df)}")
print()

def download_2d(cid, outfile):

    url = (
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
        f"compound/CID/{cid}/SDF"
    )

    try:

        r = requests.get(url, timeout=60)

        if r.status_code == 200 and len(r.text) > 100:

            outfile.write_text(r.text)

            return "SUCCESS", ""

        return "FAILED", f"HTTP {r.status_code}"

    except Exception as e:

        return "FAILED", str(e)


results = []

success = 0
failed = 0
nocid = 0

for _, row in df.iterrows():

    ligand = row["LigandID"]
    name = row["Name"]
    cid = row["PubChemCID"]

    if pd.isna(cid):

        nocid += 1

        results.append({
            "LigandID": ligand,
            "Status": "NO_CID",
            "Error": "Missing CID"
        })

        print(f"{ligand:<12} NO_CID")

        continue

    cid = int(cid)

    outfile = SDF_DIR / f"{ligand}_{cid}.sdf"

    status, err = download_2d(cid, outfile)

    if status == "SUCCESS":
        success += 1
    else:
        failed += 1

    results.append({
        "LigandID": ligand,
        "PubChemCID": cid,
        "Status": status,
        "Error": err
    })

    print(f"{ligand:<12} {status}")

    time.sleep(0.2)

report = pd.DataFrame(results)

report.to_csv(REPORT, index=False)

print()
print("="*80)
print("SUMMARY")
print("="*80)

print("Recovered :", success)
print("Still failed :", failed)
print("No CID :", nocid)

print()

print(REPORT)
