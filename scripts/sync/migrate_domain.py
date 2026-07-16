from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs" / "domain_registry"

def ensure_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        print(f"[SKIP] {path}")
        return
    path.write_text(content, encoding="utf-8")
    print(f"[CREATE] {path}")

for reg_file in sorted(REGISTRY.glob("*.json")):

    reg = json.loads(reg_file.read_text(encoding="utf-8"))

    if not reg.get("freeze", False):
        continue

    coverage = ROOT / reg["coverage_analysis"]
    srr = ROOT / reg["srr"]

    ensure_file(
        coverage,
f"""# GOHIF {reg['name']} Coverage Analysis

Version: {reg['version']}

Status: Frozen

> Legacy domain migrated to Governance v2.

## Registered Datasets

{chr(10).join(f"- {d}" for d in reg["datasets"])}

## Recommendation

Freeze maintained following governance migration.
"""
    )

    ensure_file(
        srr,
f"""# Scientific Review Record

ID: SRR-{reg['id'].upper()}

Domain: {reg['name']}

Status: Frozen

## Scope

Legacy domain migrated into Governance v2.

## Registered Datasets

{chr(10).join(f"- {d}" for d in reg["datasets"])}

## Recommendation

Approved.
"""
    )

print("\nMigration complete.")
