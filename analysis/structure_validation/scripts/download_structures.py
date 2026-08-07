#!/usr/bin/env python3

"""
GOHIF Phase II
Phase 2 – Automated Structure Download

Downloads experimental PDB structures listed in
Selected_Structures.csv

Author: GOHIF
"""

from pathlib import Path
import requests
import pandas as pd
from tqdm import tqdm
import logging

BASE = Path.home() / "GOHIF" / "analysis" / "structure_validation"

CSV = BASE / "selected_structures" / "Selected_Structures.csv"

PDB_DIR = BASE / "pdb" / "raw"

LOG_DIR = BASE / "download_logs"

MANIFEST = BASE / "pdb" / "metadata" / "structure_manifest.csv"

LOGFILE = LOG_DIR / "download.log"

PDB_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

df = pd.read_csv(CSV)

manifest = []

print("="*70)
print("GOHIF Phase II")
print("Downloading Experimental Structures")
print("="*70)

for _, row in tqdm(df.iterrows(), total=len(df)):

    protein = str(row["Protein"]).strip()

    pdb = str(row["PDB ID"]).strip().upper()

    url = f"https://files.rcsb.org/download/{pdb}.pdb"

    outfile = PDB_DIR / f"{pdb}.pdb"

    status = "SUCCESS"

    message = ""

    if outfile.exists():

        status = "EXISTS"

        message = "Already downloaded"

    else:

        try:

            r = requests.get(url, timeout=60)

            if r.status_code == 200:

                outfile.write_bytes(r.content)

                message = "Downloaded"

            else:

                status = "FAILED"

                message = f"HTTP {r.status_code}"

        except Exception as e:

            status = "FAILED"

            message = str(e)

    manifest.append({

        "Protein": protein,

        "PDB_ID": pdb,

        "Status": status,

        "Message": message,

        "File": str(outfile)

    })

    logging.info(f"{protein} {pdb} {status} {message}")

manifest = pd.DataFrame(manifest)

manifest.to_csv(MANIFEST,index=False)

print()

print("="*70)

print("Download Complete")

print("="*70)

print(manifest["Status"].value_counts())

print()

print(f"Manifest saved to:\n{MANIFEST}")

print("="*70)
