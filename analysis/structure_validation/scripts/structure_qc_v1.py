#!/usr/bin/env python3

"""
GOHIF Phase II
Phase 3 – Structure Quality Control

Author: GOHIF

This script performs automated quality control on all downloaded PDB
structures and generates publication-ready QC reports.
"""

from pathlib import Path
from Bio.PDB import PDBParser
import pandas as pd

BASE = Path.home() / "GOHIF" / "analysis" / "structure_validation"

PDB_DIR = BASE / "pdb" / "raw"

QC_DIR = BASE / "qc"

REPORT_DIR = BASE / "reports"

STAT_DIR = BASE / "statistics"

QC_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
STAT_DIR.mkdir(parents=True, exist_ok=True)

parser = PDBParser(QUIET=True)

results = []

print("="*80)
print("GOHIF Phase II")
print("Structure Quality Control")
print("="*80)

for pdb_file in sorted(PDB_DIR.glob("*.pdb")):

    pdb_id = pdb_file.stem

    try:

        structure = parser.get_structure(pdb_id, pdb_file)

        models = len(list(structure))

        chains = set()

        residues = 0

        hetatm = 0

        waters = 0

        atoms = 0

        for model in structure:

            for chain in model:

                chains.add(chain.id)

                for residue in chain:

                    if residue.id[0] == " ":

                        residues += 1

                    elif residue.id[0].startswith("H"):

                        hetatm += 1

                    elif residue.id[0] == "W":

                        waters += 1

                    atoms += len(residue)

        qc_status = "PASS"

        if residues < 100:
            qc_status = "REVIEW"

        results.append({

            "PDB_ID": pdb_id,

            "Models": models,

            "Chains": ",".join(sorted(chains)),

            "Residues": residues,

            "Atoms": atoms,

            "HETATM": hetatm,

            "Waters": waters,

            "QC_Status": qc_status

        })

        print(f"{pdb_id:6s}  PASS")

    except Exception as e:

        results.append({

            "PDB_ID": pdb_id,

            "Models": None,

            "Chains": "",

            "Residues": 0,

            "Atoms": 0,

            "HETATM": 0,

            "Waters": 0,

            "QC_Status": "FAILED"

        })

        print(f"{pdb_id:6s}  FAILED")

df = pd.DataFrame(results)

csv_file = STAT_DIR / "Structure_QC_Report.csv"

txt_file = STAT_DIR / "Structure_QC_Summary.txt"

html_file = REPORT_DIR / "Structure_QC_Report.html"

df.to_csv(csv_file,index=False)

df.to_html(html_file,index=False)

with open(txt_file,"w") as f:

    f.write("GOHIF Phase II\n")

    f.write("Structure QC Summary\n\n")

    f.write(df["QC_Status"].value_counts().to_string())

print()

print("="*80)

print(df["QC_Status"].value_counts())

print()

print(f"CSV  : {csv_file}")

print(f"HTML : {html_file}")

print(f"TEXT : {txt_file}")

print("="*80)
