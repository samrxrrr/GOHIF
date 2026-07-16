from pathlib import Path
from datetime import datetime

from validator import validate

import sync_mdi
import sync_mrd
import sync_mdd
import sync_readme
import sync_reports
import sync_decisions

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "build" / "phase2"
BUILD.mkdir(parents=True, exist_ok=True)

LOG = BUILD / "Synchronization_Run.log"

def log(msg):
    print(msg)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

# ---------------------------------------------------------------------

with open(LOG, "w", encoding="utf-8") as f:
    f.write("GOHIF Synchronization Log\n")
    f.write(f"Started: {datetime.now()}\n\n")

log("=" * 72)
log("GOHIF PHASE 2 SYNCHRONIZATION ENGINE")
log("=" * 72)

log("")
log("[1/7] Validation")

if not validate():
    log("")
    log("Synchronization aborted due to validation failure.")
    raise SystemExit(1)

log("")
log("[2/7] Master Dataset Inventory")
sync_mdi.run()

log("")
log("[3/7] Master Research Document")
sync_mrd.run()

log("")
log("[4/7] Master Development Document")
sync_mdd.run()

log("")
log("[5/7] README")
sync_readme.run()

log("")
log("[6/7] Reports")
sync_reports.run()

log("")
log("[7/7] Decision Summary")
sync_decisions.run()

log("")
log("=" * 72)
log("Synchronization completed successfully.")
log("=" * 72)
