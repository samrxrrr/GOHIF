#!/usr/bin/env python3

from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem

ROOT = Path.home() / "GOHIF"
SDF_DIR = ROOT / "analysis/structure_validation/ligands/sdf"

targets = [
    "GOHIF-033",
    "GOHIF-052",
    "GOHIF-093",
    "GOHIF-158",
    "GOHIF-214",
]

print("=" * 80)
print("GOHIF - RDKit 3D Recovery")
print("=" * 80)

for ligand in targets:

    files = list(SDF_DIR.glob(f"{ligand}_*.sdf"))

    if not files:
        print(f"{ligand:<12} MISSING")
        continue

    sdf = files[0]

    try:
        mol = Chem.MolFromMolFile(str(sdf), removeHs=False)

        if mol is None:
            print(f"{ligand:<12} FAILED")
            continue

        mol = Chem.AddHs(mol)

        AllChem.EmbedMolecule(
            mol,
            AllChem.ETKDGv3()
        )

        AllChem.MMFFOptimizeMolecule(mol)

        writer = Chem.SDWriter(str(sdf))
        writer.write(mol)
        writer.close()

        print(f"{ligand:<12} SUCCESS")

    except Exception as e:
        print(f"{ligand:<12} FAILED")
        print(e)

print("=" * 80)
