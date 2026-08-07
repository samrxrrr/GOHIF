#!/usr/bin/env python3

from pathlib import Path
import pandas as pd

ROOT = Path.home() / "GOHIF"

RECEPTORS = ROOT / "analysis/structure_validation/prepared_receptors/pdbqt"
LIGANDS = ROOT / "analysis/structure_validation/ligands/pdbqt"
CONFIGS = ROOT / "analysis/structure_validation/vina_configs"

OUTDIR = ROOT / "analysis/structure_validation/docking"
OUTDIR.mkdir(parents=True, exist_ok=True)

rows = []

for receptor in sorted(RECEPTORS.glob("*.pdbqt")):

    config = CONFIGS / f"{receptor.stem}.conf"

    for ligand in sorted(LIGANDS.glob("*.pdbqt")):

        out = OUTDIR / "results" / receptor.stem / f"{ligand.stem}.pdbqt"

        log = OUTDIR / "logs" / receptor.stem / f"{ligand.stem}.log"

        rows.append({
            "Receptor": receptor.stem,
            "Ligand": ligand.stem,
            "ReceptorPDBQT": str(receptor),
            "LigandPDBQT": str(ligand),
            "Config": str(config),
            "Output": str(out),
            "Log": str(log)
        })

df = pd.DataFrame(rows)

manifest = OUTDIR / "Docking_Manifest.csv"

df.to_csv(manifest, index=False)

print("="*80)
print("GOHIF Docking Manifest")
print("="*80)
print("Rows:", len(df))
print("Manifest:", manifest)
