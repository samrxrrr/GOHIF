#!/usr/bin/env python3

"""
=========================================================================
GOHIF Phase II
Receptor Preparation Pipeline

Part 1
Structure Loading + Chain Extraction

Author : GOHIF
=========================================================================

Input

Frozen_Chain_Selection.csv

Raw Structures (.pdb/.cif)

Output

prepared_receptors/raw/

=========================================================================

"""

from pathlib import Path

import pandas as pd

from Bio.PDB import PDBParser
from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.PDB import PDBIO, Select, Select

##############################################################################

BASE = Path.home()/"GOHIF"/"analysis"/"structure_validation"

RAW = BASE/"pdb"/"raw"

PREP = BASE/"prepared_receptors"

RAW_OUT = PREP/"raw"

LOGS = PREP/"logs"

REPORTS = PREP/"reports"

RAW_OUT.mkdir(parents=True,exist_ok=True)
LOGS.mkdir(parents=True,exist_ok=True)
REPORTS.mkdir(parents=True,exist_ok=True)

##############################################################################

CHAIN_TABLE = REPORTS/"Frozen_Chain_Selection.csv"

CHAINS = pd.read_csv(CHAIN_TABLE)

##############################################################################

PDB = PDBParser(QUIET=True)

MMCIF = MMCIFParser(QUIET=True)

IO = PDBIO()

##############################################################################

print("="*80)
print("GOHIF Phase II")
print("Receptor Preparation")
print("Part 1 : Chain Extraction")
print("="*80)

manifest=[]

##############################################################################
##############################################################################

class ChainSelect(Select):

    def __init__(self, target):
        self.target = target

    def accept_chain(self, chain):
        return chain.id == self.target

##############################################################################

for _,row in CHAINS.iterrows():

    protein=row["Protein"]

    pdb=row["PDB_ID"]

    chain=str(row["Selected_Chains"]).strip()

    if chain=="nan":

        manifest.append({

            "Protein":protein,

            "PDB_ID":pdb,

            "Status":"SKIPPED",

            "Reason":"No chain selected"

        })

        continue

    pdb_file=RAW/f"{pdb}.pdb"

    cif_file=RAW/f"{pdb}.cif"

    try:

        if pdb_file.exists():

            structure=PDB.get_structure(pdb,pdb_file)

        elif cif_file.exists():

            structure=MMCIF.get_structure(pdb,cif_file)

        else:

            raise FileNotFoundError

        IO.set_structure(structure)

        outfile=RAW_OUT/f"{protein}_{pdb}_chain_{chain}.pdb"

        IO.save(str(outfile),ChainSelect(chain))

        manifest.append({

            "Protein":protein,

            "PDB_ID":pdb,

            "Chain":chain,

            "Output":outfile.name,

            "Status":"SUCCESS"

        })

        print(f"{protein:20s} {chain}  SUCCESS")

    except Exception as e:

        manifest.append({

            "Protein":protein,

            "PDB_ID":pdb,

            "Chain":chain,

            "Status":"FAILED",

            "Reason":str(e)

        })

        print(f"{protein:20s} FAILED -> {e}")

##############################################################################

manifest=pd.DataFrame(manifest)

manifest.to_csv(

REPORTS/"Chain_Extraction_Report.csv",

index=False

)

print()

print("="*80)

print("CHAIN EXTRACTION COMPLETE")

print("="*80)

print(manifest["Status"].value_counts())

print()

print("Report:")

print(REPORTS/"Chain_Extraction_Report.csv")

print("="*80)
