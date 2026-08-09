#!/usr/bin/env python3

from pathlib import Path
import subprocess
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

ROOT = Path.home() / "GOHIF"

MANIFEST = ROOT / "analysis/structure_validation/docking/Docking_Manifest.csv"

df = pd.read_csv(MANIFEST)

N_WORKERS = 1

print("=" * 80)
print("GOHIF Phase II")
print("Parallel AutoDock Vina Docking")
print("=" * 80)
print(f"Jobs    : {len(df)}")
print(f"Workers : {N_WORKERS}")
print()

completed = 0
skipped = 0
failed = 0


def run_job(row):

    out_file = Path(row["Output"])
    log_file = Path(row["Log"])

    out_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    if out_file.exists() and out_file.stat().st_size > 0:
        return ("SKIPPED", row["Receptor"], row["Ligand"])

    cmd = [
        "vina",
        "--receptor", row["ReceptorPDBQT"],
        "--ligand", row["LigandPDBQT"],
        "--config", row["Config"],
        "--out", str(out_file)
    ]

    try:
        with open(log_file, "w") as log:
            subprocess.run(
                cmd,
                stdout=log,
                stderr=log,
                check=True
            )
        return ("SUCCESS", row["Receptor"], row["Ligand"])

    except Exception:
        return ("FAILED", row["Receptor"], row["Ligand"])


with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:

    futures = [executor.submit(run_job, row) for _, row in df.iterrows()]

    total = len(futures)

    for i, future in enumerate(as_completed(futures), 1):

        status, receptor, ligand = future.result()

        if status == "SUCCESS":
            completed += 1
        elif status == "SKIPPED":
            skipped += 1
        else:
            failed += 1

        print(
            f"[{i:5d}/{total}] "
            f"{status:<8} "
            f"{receptor:<30} "
            f"{ligand}"
        )

print()
print("=" * 80)
print("FINAL SUMMARY")
print("=" * 80)
print("Completed :", completed)
print("Skipped   :", skipped)
print("Failed    :", failed)
