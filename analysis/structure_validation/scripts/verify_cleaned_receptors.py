#!/usr/bin/env python3

"""
========================================================================
GOHIF Phase II

Verification of Cleaned Receptors

Checks:

✓ Waters removed
✓ HETATM removal
✓ Metals retained
✓ Protein residues present

========================================================================
"""

from pathlib import Path

import pandas as pd

from Bio.PDB import PDBParser

########################################################################

BASE = Path.home()/"GOHIF"/"analysis"/"structure_validation"

CLEAN = BASE/"prepared_receptors"/"cleaned"

REPORT = BASE/"prepared_receptors"/"reports"

REPORT.mkdir(parents=True,exist_ok=True)

FILES = sorted(CLEAN.glob("*.pdb"))

PARSER = PDBParser(QUIET=True)

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

RESULTS=[]

print("="*80)
print("GOHIF")
print("Cleaned Receptor Verification")
print("="*80)
print("Structures :",len(FILES))
print()
########################################################################

for pdb in FILES:

    structure=PARSER.get_structure(pdb.stem,pdb)

    protein=0

    waters=0

    metals=0

    other_het=0

    for model in structure:

        for chain in model:

            for residue in chain:

                flag=residue.id[0]

                if flag==" ":

                    protein+=1

                    continue

                if flag=="W":

                    waters+=1

                    continue

                res=residue.get_resname().strip().upper()

                if res in KEEP:

                    metals+=1

                else:

                    other_het+=1

    status="PASS"

    if waters>0:

        status="CHECK"

    if other_het>0:

        status="CHECK"

    RESULTS.append({

        "Protein":pdb.stem,

        "ProteinResidues":protein,

        "Waters":waters,

        "Metals":metals,

        "Other_HETATM":other_het,

        "Status":status

    })

    print(

        f"{pdb.stem:40s}"

        f"{status}"

    )

########################################################################

df=pd.DataFrame(RESULTS)

outfile=REPORT/"Cleaning_Validation_Report.csv"

df.to_csv(outfile,index=False)

print()

print("="*80)

print(df["Status"].value_counts())

print()

print("Validation report:")

print(outfile)

print("="*80)
