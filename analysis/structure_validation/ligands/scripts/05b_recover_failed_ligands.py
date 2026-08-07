#!/usr/bin/env python3

from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

ROOT = Path.home() / "GOHIF"

SDF_DIR = ROOT / "analysis/structure_validation/ligands/sdf"

failed = [
"GOHIF-029",
"GOHIF-050",
"GOHIF-052",
"GOHIF-060",
"GOHIF-061",
"GOHIF-062",
"GOHIF-063",
"GOHIF-079",
"GOHIF-080",
"GOHIF-089",
"GOHIF-097",
"GOHIF-146",
"GOHIF-194",
"GOHIF-207",
"GOHIF-247",
"GOHIF-250"
]

print("="*80)
print("GOHIF Failed Ligand Recovery")
print("="*80)

for lig in failed:

    files = list(SDF_DIR.glob(f"{lig}_*.sdf"))

    if not files:
        print(lig, "NOT FOUND")
        continue

    sdf = files[0]

    try:

        mol = Chem.MolFromMolFile(str(sdf), removeHs=False)

        if mol is None:
            print(lig, "FAILED_READ")
            continue

        parent = rdMolStandardize.FragmentParent(mol)

        parent = Chem.AddHs(parent)

        AllChem.EmbedMolecule(parent, AllChem.ETKDGv3())

        try:
            AllChem.MMFFOptimizeMolecule(parent)
        except:
            try:
                AllChem.UFFOptimizeMolecule(parent)
            except:
                pass

        writer = Chem.SDWriter(str(sdf))
        writer.write(parent)
        writer.close()

        print(lig, "RECOVERED")

    except Exception as e:
        print(lig, "FAILED", e)
