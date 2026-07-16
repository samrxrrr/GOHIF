from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

REGISTRY = ROOT / "docs" / "domain_registry"

OUTPUT = ROOT / "build" / "phase2" / "Decision_Summary.md"

domains = []

for f in sorted(REGISTRY.glob("*.json")):
    with open(f, encoding="utf-8") as fp:
        domains.append(json.load(fp))

with open(OUTPUT, "w", encoding="utf-8") as out:

    out.write("# GOHIF Decision Summary\n\n")

    out.write("This file summarizes domain freeze decisions.\n\n")

    for d in domains:

        out.write(f"## {d['name']}\n\n")

        out.write(f"- Status: {d['status']}\n")
        out.write(f"- Version: {d['version']}\n")
        out.write(f"- Frozen: {d['freeze']}\n")
        out.write(f"- Registered Datasets: {len(d['datasets'])}\n\n")

print(f"[OK] Generated {OUTPUT}")
