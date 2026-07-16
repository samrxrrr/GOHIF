from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

REGISTRY = ROOT / "docs" / "domain_registry"

BUILD = ROOT / "build" / "phase2"
BUILD.mkdir(parents=True, exist_ok=True)

OUTPUT = BUILD / "Master_Research_Document.md"

chapter_order = [
    "human_health",
    "animal_health",
    "environmental_health",
    "food_chain",
    "plant_health",
    "genomics",
    "knowledge_resources",
    "metadata",
    "validation"
]

TITLE_MAP = {
    "human_health":"Human Health",
    "animal_health":"Animal Health",
    "environmental_health":"Environmental Health",
    "food_chain":"Food Chain",
    "plant_health":"Plant Health",
    "genomics":"Genomics & Molecular Evidence",
    "knowledge_resources":"Knowledge Resources",
    "metadata":"Metadata & Data Quality",
    "validation":"Validation & Benchmarking"
}

def append_file(out, path):
    if path.exists():
        out.write(path.read_text(encoding="utf-8"))
        out.write("\n\n")
    else:
        out.write(f"> Source file missing: {path}\n\n")

with open(OUTPUT, "w", encoding="utf-8") as out:

    out.write("# GOHIF Master Research Document\n\n")
    out.write("**Status:** Auto-generated\n\n")
    out.write("---\n\n")

    mdi = ROOT / "build" / "phase2" / "Master_Dataset_Inventory.md"
    if not mdi.exists():
        mdi = ROOT / "datasets" / "master_inventory" / "Master_Dataset_Inventory.md"

    if mdi.exists():
        out.write("## Master Dataset Inventory Summary\n\n")
        append_file(out, mdi)

    for domain in chapter_order:

        reg_file = REGISTRY / f"{domain}.json"

        if not reg_file.exists():
            continue

        reg = json.loads(reg_file.read_text())

        out.write("\n---\n\n")
        out.write(f"# {TITLE_MAP.get(domain, domain)}\n\n")

        if not reg.get("freeze", False):
            out.write("**Status:** Pending\n\n")
            continue

        out.write("## Coverage Analysis\n\n")
        cov = ROOT / reg["coverage_analysis"]
        append_file(out, cov)

        out.write("## Scientific Review Record\n\n")
        srr = ROOT / reg["srr"]
        append_file(out, srr)

print(f"[OK] Generated {OUTPUT}")
