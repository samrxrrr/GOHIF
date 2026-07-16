from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

REGISTRY = ROOT / "docs" / "domain_registry"
BUILD = ROOT / "build" / "phase2"

BUILD.mkdir(parents=True, exist_ok=True)

OUTPUT = BUILD / "Master_Development_Document.md"

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

ORDER = [
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

def append_file(out, path):
    if path.exists():
        out.write(path.read_text(encoding="utf-8"))
        out.write("\n\n")
    else:
        out.write(f"> Source file missing: {path}\n\n")

with open(OUTPUT, "w", encoding="utf-8") as out:

    out.write("# GOHIF Master Development Document\n\n")
    out.write("**Status:** Auto-generated\n\n")
    out.write("---\n\n")

    front = ROOT / "docs" / "MDD" / "chapters" / "00_Front_Matter.md"
    if front.exists():
        append_file(out, front)

    arch = ROOT / "docs" / "MDD" / "chapters" / "01_System_Architecture.md"
    if arch.exists():
        append_file(out, arch)

    repo = ROOT / "docs" / "MDD" / "chapters" / "02_Repository_Architecture.md"
    if repo.exists():
        append_file(out, repo)

    for domain in ORDER:

        reg_file = REGISTRY / f"{domain}.json"

        if not reg_file.exists():
            continue

        reg = json.loads(reg_file.read_text())

        out.write("\n---\n\n")
        out.write(f"# {TITLE_MAP.get(domain, domain)}\n\n")

        if not reg.get("freeze", False):
            out.write("**Status:** Pending\n\n")
            continue

        out.write(f"**Status:** Frozen (v{reg['version']})\n\n")
        out.write(f"Datasets Registered: {len(reg['datasets'])}\n\n")

        chapter = ROOT / "docs" / "MDD" / "chapters"

        mapping = {
            "human_health":"06_Human_Health.md",
            "animal_health":"07_Animal_Health.md",
            "environmental_health":"08_Environmental_Health.md",
            "food_chain":"09_Food_Chain.md",
            "plant_health":"10_Plant_Health.md",
            "genomics":"11_Genomics.md",
            "metadata":"12_Evidence_Ontology.md",
            "knowledge_resources":"13_Evidence_Harmonization.md",
            "validation":"15_Validation_Framework.md"
        }

        if domain in mapping:
            append_file(out, chapter / mapping[domain])

print(f"[OK] Generated {OUTPUT}")
