from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs" / "domain_registry"

def info(msg):
    print(f"[INFO] {msg}")

def ok(msg):
    print(f"[ OK ] {msg}")

def fail(msg):
    print(f"[FAIL] {msg}")

def validate():

    info("Loading domain registry...")

    registry_files = sorted(REGISTRY.glob("*.json"))

    if not registry_files:
        fail("No domain registry found.")
        return False

    success = True

    for reg in registry_files:

        with open(reg, "r", encoding="utf-8") as f:
            domain = json.load(f)

        name = domain["id"]

        if not domain.get("freeze", False):
            print(f"[SKIP] {name} (not frozen)")
            continue

        print(f"\n[DOMAIN] {domain['name']}")

        coverage = ROOT / domain["coverage_analysis"]
        srr = ROOT / domain["srr"]

        if coverage.exists():
            ok("Coverage Analysis")
        else:
            fail(f"Missing Coverage Analysis: {coverage}")
            success = False

        if srr.exists():
            ok("Scientific Review Record")
        else:
            fail(f"Missing SRR: {srr}")
            success = False

    return success
