from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]

DOMAIN_REGISTRY = ROOT / "docs" / "domain_registry"
DATASET_REGISTRY = ROOT / "data" / "registry" / "datasets"

BUILD = ROOT / "build" / "phase2"
BUILD.mkdir(parents=True, exist_ok=True)

REPORT = BUILD / "Synchronization_Report.md"

domains = []
datasets = []

for f in sorted(DOMAIN_REGISTRY.glob("*.json")):
    with open(f, encoding="utf-8") as fp:
        domains.append(json.load(fp))

for f in sorted(DATASET_REGISTRY.glob("*.json")):
    with open(f, encoding="utf-8") as fp:
        datasets.append(json.load(fp))

frozen = [d for d in domains if d.get("freeze", False)]

with open(REPORT, "w", encoding="utf-8") as out:

    out.write("# GOHIF Phase 2 Synchronization Report\n\n")

    out.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    out.write("## Summary\n\n")
    out.write(f"- Registered Domains: {len(domains)}\n")
    out.write(f"- Frozen Domains: {len(frozen)}\n")
    out.write(f"- Registered Datasets: {len(datasets)}\n\n")

    out.write("## Frozen Domains\n\n")

    for d in frozen:
        out.write(f"- {d['name']} (v{d['version']})\n")

    out.write("\n## Generated Artifacts\n\n")
    out.write("- Master Dataset Inventory\n")
    out.write("- Master Research Document\n")
    out.write("- Master Development Document\n")
    out.write("- README\n")
    out.write("- Synchronization Report\n")

print(f"[OK] Generated {REPORT}")
