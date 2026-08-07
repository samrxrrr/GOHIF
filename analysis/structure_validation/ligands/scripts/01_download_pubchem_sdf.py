#!/usr/bin/env python3

"""
GOHIF Phase II
Step 01
Download 3D SDF structures from PubChem

Author: GOHIF
"""

from pathlib import Path
import pandas as pd
import requests
import time

# =============================================================================
# PATHS
# =============================================================================

ROOT = Path.home() / "GOHIF"

LIBRARY = (
    ROOT /
    "analysis/structure_validation/selected_structures/GOHIF_Ligand_Library_250.xlsx"
)

OUTPUT_DIR = (
    ROOT /
    "analysis/structure_validation/ligands/sdf"
)

REPORT_DIR = (
    ROOT /
    "analysis/structure_validation/ligands/reports"
)

LOG_DIR = (
    ROOT /
    "analysis/structure_validation/ligands/logs"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

REPORT = REPORT_DIR / "PubChem_Download_Report.csv"

print("="*80)
print("GOHIF Phase II")
print("PubChem 3D Downloader")
print("="*80)

df = pd.read_excel(LIBRARY)

print(f"Ligands : {len(df)}")
print()

# =============================================================================
# DOWNLOAD FUNCTION
# =============================================================================

def download_pubchem_sdf(cid, outfile):

    url = (
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
        f"compound/CID/{cid}/SDF?record_type=3d"
    )

    try:

        r = requests.get(url, timeout=60)

        if r.status_code == 200 and len(r.text) > 100:

            outfile.write_text(r.text)

            return "SUCCESS", ""

        return "FAILED", f"HTTP {r.status_code}"

    except Exception as e:

        return "FAILED", str(e)


# =============================================================================
# DOWNLOAD LOOP
# =============================================================================

results = []

success = 0
failed = 0
missing = 0

print("Starting downloads...\n")

# =============================================================================
# PROCESS EACH LIGAND
# =============================================================================

for _, row in df.iterrows():

    ligand_id = row["LigandID"]
    name = row["Name"]
    cid = row["PubChemCID"]

    if pd.isna(cid):

        results.append({
            "LigandID": ligand_id,
            "Name": name,
            "PubChemCID": "",
            "Status": "NO_CID",
            "File": "",
            "Error": "Missing PubChem CID"
        })

        missing += 1

        print(f"{ligand_id:<12} NO_CID")

        continue

    cid = int(cid)

    outfile = OUTPUT_DIR / f"{ligand_id}_{cid}.sdf"

    status, error = download_pubchem_sdf(cid, outfile)

    if status == "SUCCESS":
        success += 1
    else:
        failed += 1

    results.append({
        "LigandID": ligand_id,
        "Name": name,
        "PubChemCID": cid,
        "Status": status,
        "File": str(outfile) if outfile.exists() else "",
        "Error": error
    })

    print(f"{ligand_id:<12} {status}")

    time.sleep(0.2)
# =============================================================================
# SAVE REPORT
# =============================================================================

report = pd.DataFrame(results)

report = report.sort_values(
    by=["Status", "LigandID"],
    ascending=[True, True]
)

report.to_csv(REPORT, index=False)

# =============================================================================
# SUMMARY
# =============================================================================

summary_file = REPORT_DIR / "Download_Summary.txt"

with open(summary_file, "w") as f:

    f.write("=" * 80 + "\n")
    f.write("GOHIF Phase II\n")
    f.write("PubChem 3D Download Summary\n")
    f.write("=" * 80 + "\n\n")

    f.write(f"Total Ligands : {len(df)}\n")
    f.write(f"Downloaded    : {success}\n")
    f.write(f"Failed        : {failed}\n")
    f.write(f"Missing CID   : {missing}\n")

# =============================================================================
# FAILED DOWNLOADS
# =============================================================================

failed_df = report[report["Status"] != "SUCCESS"]

if len(failed_df) > 0:

    failed_file = REPORT_DIR / "Failed_Downloads.csv"

    failed_df.to_csv(
        failed_file,
        index=False
    )

    print()
    print("Failed downloads saved:")
    print(failed_file)

# =============================================================================
# DOWNLOAD STATISTICS
# =============================================================================

success_pct = (success / len(df)) * 100

print()
print("=" * 80)
print("DOWNLOAD SUMMARY")
print("=" * 80)

print(f"Total Ligands : {len(df)}")
print(f"Downloaded    : {success}")
print(f"Failed        : {failed}")
print(f"Missing CID   : {missing}")
print(f"Success Rate  : {success_pct:.2f}%")

print()
print("Report:")
print(REPORT)

print()
print("Summary:")
print(summary_file)

# =============================================================================
# VERIFY DOWNLOADS
# =============================================================================

downloaded_files = list(OUTPUT_DIR.glob("*.sdf"))

print()
print("Downloaded SDF files :", len(downloaded_files))

# =============================================================================
# END
# =============================================================================

print()
print("=" * 80)
print("GOHIF PubChem Download Complete")
print("=" * 80)
