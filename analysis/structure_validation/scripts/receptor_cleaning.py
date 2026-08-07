#!/usr/bin/env python3

"""
========================================================================
GOHIF Phase II

Receptor Cleaning Pipeline

Version 2.0

========================================================================
"""

from pathlib import Path

import pandas as pd

from Bio.PDB import PDBParser
from Bio.PDB import PDBIO
from Bio.PDB import Select

########################################################################

BASE = Path.home()/"GOHIF"/"analysis"/"structure_validation"

RAW_DIR = BASE/"prepared_receptors"/"raw"

CLEAN_DIR = BASE/"prepared_receptors"/"cleaned"

REPORT_DIR = BASE/"prepared_receptors"/"reports"

LOG_DIR = BASE/"prepared_receptors"/"logs"

CLEAN_DIR.mkdir(parents=True,exist_ok=True)

REPORT_DIR.mkdir(parents=True,exist_ok=True)

LOG_DIR.mkdir(parents=True,exist_ok=True)

########################################################################

REMOVE = {

"HOH",

"WAT",

"GOL",

"PEG",

"MPD",

"EDO",

"DMS",

"MES",

"TRS"

}

KEEP = {

"ZN",

"MG",

"MN",

"CA",

"FE",

"NI",

"CO",

"CU",

"NA",

"K"

}

########################################################################

PARSER = PDBParser(QUIET=True)

MANIFEST = []

print("="*80)

print("GOHIF Receptor Cleaning v2")

print("="*80)

FILES = sorted(RAW_DIR.glob("*.pdb"))

print("Structures Found :",len(FILES))

print("="*80)

########################################################################
# Residue Selection Class
########################################################################

class CleanSelect(Select):

    def accept_model(self, model):
        return True

    def accept_chain(self, chain):
        return True

    def accept_residue(self, residue):

        hetflag = residue.id[0]

        # ------------------------------------------------------------
        # Keep all standard amino acids
        # ------------------------------------------------------------

        if hetflag == " ":
            return True

        # ------------------------------------------------------------
        # Remove waters
        # ------------------------------------------------------------

        if hetflag == "W":
            return False

        resname = residue.get_resname().strip().upper()

        # ------------------------------------------------------------
        # Remove crystallization compounds
        # ------------------------------------------------------------

        if resname in REMOVE:
            return False

        # ------------------------------------------------------------
        # Keep catalytic metal ions
        # ------------------------------------------------------------

        if resname in KEEP:
            return True

        # ------------------------------------------------------------
        # Remove every other HETATM
        # ------------------------------------------------------------

        return False


########################################################################
# Clean One Structure
########################################################################

def clean_structure(input_file, output_file):

    structure = PARSER.get_structure(
        input_file.stem,
        str(input_file)
    )

    io = PDBIO()

    io.set_structure(structure)

    io.save(
        str(output_file),
        CleanSelect()
    )

    return output_file.exists()

########################################################################
# Main Cleaning Loop
########################################################################

for pdb in FILES:

    outfile = CLEAN_DIR / pdb.name

    try:

        ok = clean_structure(
            pdb,
            outfile
        )

        if ok:

            MANIFEST.append({

                "Protein": pdb.stem,

                "Status": "SUCCESS",

                "Output": outfile.name

            })

            print(f"{pdb.stem:<40} SUCCESS")

        else:

            MANIFEST.append({

                "Protein": pdb.stem,

                "Status": "FAILED",

                "Reason": "Output file missing"

            })

            print(f"{pdb.stem:<40} FAILED")

    except Exception as e:

        MANIFEST.append({

            "Protein": pdb.stem,

            "Status": "FAILED",

            "Reason": str(e)

        })

        print(f"{pdb.stem:<40} FAILED -> {e}")

########################################################################
# Generate Report
########################################################################

manifest = pd.DataFrame(MANIFEST)

REPORT_FILE = REPORT_DIR / "Receptor_Cleaning_Report.csv"

manifest.to_csv(
    REPORT_FILE,
    index=False
)

########################################################################
# Summary
########################################################################

print()

print("=" * 80)
print("GOHIF Receptor Cleaning Complete")
print("=" * 80)

if len(manifest) > 0:

    print()

    print(manifest["Status"].value_counts())

    success = (manifest["Status"] == "SUCCESS").sum()

    failed = (manifest["Status"] == "FAILED").sum()

    print()

    print(f"Successful : {success}")

    print(f"Failed     : {failed}")

else:

    print("No structures processed.")

print()

print("Cleaned structures directory:")

print(CLEAN_DIR)

print()

print("Cleaning report:")

print(REPORT_FILE)

print("=" * 80)
