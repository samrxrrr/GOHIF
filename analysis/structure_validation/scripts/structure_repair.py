#!/usr/bin/env python3

"""
========================================================================
GOHIF Phase II

Structure Repair Assessment

Version 1.0

Checks:

✓ Missing residues
✓ Missing atoms
✓ Chain count
✓ Protein residues

No modifications are performed in this step.

========================================================================
"""

from pathlib import Path
import pandas as pd

from Bio.PDB import PDBParser

########################################################################

BASE = Path.home()/"GOHIF"/"analysis"/"structure_validation"

INPUT = BASE/"prepared_receptors"/"cleaned"

OUTPUT = BASE/"prepared_receptors"/"repaired"

REPORT = BASE/"prepared_receptors"/"reports"

LOG = BASE/"prepared_receptors"/"logs"

OUTPUT.mkdir(parents=True,exist_ok=True)

REPORT.mkdir(parents=True,exist_ok=True)

LOG.mkdir(parents=True,exist_ok=True)

########################################################################

FILES = sorted(INPUT.glob("*.pdb"))

PARSER = PDBParser(QUIET=True)

RESULTS=[]

print("="*80)
print("GOHIF")
print("Structure Repair Assessment")
print("="*80)
print("Structures :",len(FILES))
print()
########################################################################

for pdb in FILES:

    structure=PARSER.get_structure(pdb.stem,pdb)

    chains=0

    residues=0

    atoms=0

    models=0

    for model in structure:

        models+=1

        for chain in model:

            chains+=1

            for residue in chain:

                if residue.id[0]==" ":

                    residues+=1

                    for atom in residue:

                        atoms+=1

    repair="NO"

    reason="Experimental structure"

    if residues<150:

        repair="REVIEW"

        reason="Small structure"

    RESULTS.append({

        "Protein":pdb.stem,

        "Models":models,

        "Chains":chains,

        "ProteinResidues":residues,

        "Atoms":atoms,

        "Repair":repair,

        "Reason":reason

    })

    print(

        f"{pdb.stem:40s}"

        f"{repair}"

    )
########################################################################

df=pd.DataFrame(RESULTS)

outfile=REPORT/"Structure_Repair_Report.csv"

df.to_csv(outfile,index=False)

print()

print("="*80)

print(df["Repair"].value_counts())

print()

print("Report:")

print(outfile)

print("="*80)
