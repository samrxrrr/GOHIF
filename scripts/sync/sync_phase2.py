from validator import validate

import sync_mdi
import sync_mrd
import sync_mdd
import sync_readme
import sync_reports
import sync_decisions

print("=" * 70)
print("GOHIF PHASE 2 SYNCHRONIZATION ENGINE")
print("=" * 70)

if not validate():
    print()
    print("Synchronization aborted.")
    raise SystemExit(1)

print()
print("Validation successful.")
print()

sync_mdi.run()
sync_mrd.run()
sync_mdd.run()
sync_readme.run()
sync_reports.run()
sync_decisions.run()

print()
print("=" * 70)
print("Synchronization framework ready.")
print("=" * 70)
