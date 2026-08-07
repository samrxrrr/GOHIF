#!/usr/bin/env python3

"""
GOHIF Phase II
Automatic Chain Selection

Determines the biologically relevant chain(s)
for every downloaded receptor structure.
"""

from pathlib import Path
import pandas as pd

from Bio.PDB import PDBParser
from Bio.PDB.MMCIFParser import MMCIFParser

BASE = Path.home() / "GOHIF" / "analysis" / "structure_validation"

RAW = BASE / "pdb" / "raw"

INPUT = BASE / "prepared_receptors" / "reports" / "Chain_Selection_Template.csv"

OUTPUT = BASE / "prepared_receptors" / "reports" / "Chain_Selection_Final.csv"

df = pd.read_csv(INPUT)

pdb_parser = PDBParser(QUIET=True)
cif_parser = MMCIFParser(QUIET=True)

results = []

for _, row in df.iterrows():

    protein = row["Protein"]
    pdb = row["PDB_ID"]

    pdb_file = RAW / f"{pdb}.pdb"
    cif_file = RAW / f"{pdb}.cif"

    available = ""
    selected = ""
    reason = ""

    try:

        if pdb_file.exists():

            structure = pdb_parser.get_structure(pdb, pdb_file)

        elif cif_file.exists():

            structure = cif_parser.get_structure(pdb, cif_file)

        else:

            reason = "Structure not found"

            results.append({
                "Protein": protein,
                "PDB_ID": pdb,
                "Available_Chains": "",
                "Selected_Chains": "",
                "Reason": reason
            })

            continue

        chains = []

        residues = {}

        for model in structure:

            for chain in model:

                cid = chain.id

                chains.append(cid)

                count = 0

                for residue in chain:

                    if residue.id[0] == " ":
                        count += 1

                residues[cid] = count

            break

        chains = sorted(list(set(chains)))

        available = ",".join(chains)

        ##################################################################
        # Selection rules
        ##################################################################

        if len(chains) == 1:

            selected = chains[0]

            reason = "Single protein chain"

        else:

            max_chain = max(residues, key=residues.get)

            selected = max_chain

            reason = (
                "Largest protein chain "
                f"({residues[max_chain]} residues)"
            )

        ##################################################################
        # Known special cases
        ##################################################################

        if pdb == "7NHL":

            reason += " | REVIEW: ribosome complex"

        if len(chains) > 6:

            reason += " | REVIEW: multimeric assembly"

        results.append({

            "Protein": protein,

            "PDB_ID": pdb,

            "Available_Chains": available,

            "Selected_Chains": selected,

            "Residues_Selected": residues[selected],

            "Reason": reason

        })

    except Exception as e:

        results.append({

            "Protein": protein,

            "PDB_ID": pdb,

            "Available_Chains": "",

            "Selected_Chains": "",

            "Residues_Selected": "",

            "Reason": str(e)

        })

out = pd.DataFrame(results)

out.to_csv(OUTPUT,index=False)

print("="*80)
print("Automatic Chain Selection Complete")
print("="*80)

print(out)

print("\nSaved to:\n")

print(OUTPUT)
