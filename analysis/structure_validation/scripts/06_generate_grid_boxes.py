#!/usr/bin/env python3

from pathlib import Path
import pandas as pd

ROOT = Path.home() / "GOHIF"

PDB_DIR = ROOT / "analysis/structure_validation/prepared_receptors/cleaned"
PDBQT_DIR = ROOT / "analysis/structure_validation/prepared_receptors/pdbqt"

GRID_DIR = ROOT / "analysis/structure_validation/grid_boxes"
CONF_DIR = ROOT / "analysis/structure_validation/vina_configs"
REPORT_DIR = ROOT / "analysis/structure_validation/reports"

GRID_DIR.mkdir(parents=True, exist_ok=True)
CONF_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

records = []

padding = 8.0

print("="*80)
print("GOHIF Phase II")
print("Automatic Grid Box Generation")
print("="*80)

for pdbqt in sorted(PDBQT_DIR.glob("*.pdbqt")):

    stem = pdbqt.stem
    pdb = PDB_DIR / f"{stem}.pdb"

    if not pdb.exists():
        print(f"{stem:<40} MISSING_PDB")
        continue

    xs, ys, zs = [], [], []

    with open(pdb) as f:
        for line in f:
            if line.startswith("ATOM"):
                try:
                    xs.append(float(line[30:38]))
                    ys.append(float(line[38:46]))
                    zs.append(float(line[46:54]))
                except:
                    pass

    if not xs:
        print(f"{stem:<40} FAILED")
        continue

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    zmin, zmax = min(zs), max(zs)

    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    cz = (zmin + zmax) / 2

    sx = (xmax - xmin) + padding
    sy = (ymax - ymin) + padding
    sz = (zmax - zmin) + padding

    conf = CONF_DIR / f"{stem}.conf"

    with open(conf, "w") as out:
        out.write(f"receptor = {pdbqt}\n")
        out.write("ligand = ligand.pdbqt\n\n")
        out.write(f"center_x = {cx:.3f}\n")
        out.write(f"center_y = {cy:.3f}\n")
        out.write(f"center_z = {cz:.3f}\n\n")
        out.write(f"size_x = {sx:.3f}\n")
        out.write(f"size_y = {sy:.3f}\n")
        out.write(f"size_z = {sz:.3f}\n\n")
        out.write("exhaustiveness = 16\n")
        out.write("num_modes = 9\n")
        out.write("energy_range = 3\n")

    records.append({
        "Receptor": stem,
        "Center_X": round(cx,3),
        "Center_Y": round(cy,3),
        "Center_Z": round(cz,3),
        "Size_X": round(sx,3),
        "Size_Y": round(sy,3),
        "Size_Z": round(sz,3)
    })

    print(f"{stem:<40} SUCCESS")

df = pd.DataFrame(records)
report = REPORT_DIR / "Grid_Box_Report.csv"
df.to_csv(report, index=False)

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print("Grid boxes :", len(df))
print("Report :", report)
print("Configs:", CONF_DIR)
