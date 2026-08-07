#!/usr/bin/env python3

"""
========================================================================
GOHIF Phase II

Batch Receptor Preparation (Meeko 0.7.1)

Input:
    cleaned/*.pdb

Output:
    pdbqt/*.pdbqt

========================================================================
"""

from pathlib import Path
import subprocess
import pandas as pd

BASE = Path.home() / "GOHIF" / "analysis" / "structure_validation"

INPUT = BASE / "prepared_receptors" / "cleaned"
OUTPUT = BASE / "prepared_receptors" / "pdbqt"
REPORT = BASE / "prepared_receptors" / "reports"
LOGDIR = BASE / "prepared_receptors" / "logs"

OUTPUT.mkdir(parents=True, exist_ok=True)
REPORT.mkdir(parents=True, exist_ok=True)
LOGDIR.mkdir(parents=True, exist_ok=True)

files = sorted(INPUT.glob("*.pdb"))

results = []

print("=" * 80)
print("GOHIF Phase II")
print("Batch Receptor Preparation")
print("=" * 80)
print("Structures :", len(files))
print()

for pdb in files:

    basename = OUTPUT / pdb.stem

    logfile = LOGDIR / f"{pdb.stem}.log"

    cmd = [
        "mk_prepare_receptor.py",
        "-i",
        str(pdb),
        "-o",
        str(basename),
        "-p",
        "-a",
        "--default_altloc",
        "A",
    ]

    with open(logfile, "w") as log:

        proc = subprocess.run(
            cmd,
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
        )

    pdbqt = OUTPUT / f"{pdb.stem}.pdbqt"

    if proc.returncode == 0 and pdbqt.exists():

        status = "SUCCESS"

        removed = "NO"

        txt = logfile.read_text(errors="ignore")

        if "allow_bad_res" in txt:
            removed = "YES"

    else:

        status = "FAILED"

        removed = "NA"

    results.append({

        "Protein": pdb.stem,

        "InputPDB": pdb.name,

        "OutputPDBQT": pdbqt.name,

        "Status": status,

        "AllowBadRes": removed,

        "LogFile": logfile.name

    })

    print(f"{pdb.stem:<45}{status}")

df = pd.DataFrame(results)

report = REPORT / "Receptor_PDBQT_Report.csv"

df.to_csv(report, index=False)

print()
print("=" * 80)

print(df["Status"].value_counts())

print()

print("Report :", report)

print("PDBQT  :", OUTPUT)

print("Logs   :", LOGDIR)

print("=" * 80)
