from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

DOMAIN_REGISTRY = ROOT / "docs" / "domain_registry"
DATASET_REGISTRY = ROOT / "data" / "registry" / "datasets"

README = ROOT / "README.md"

domains = []
datasets = []

for f in sorted(DOMAIN_REGISTRY.glob("*.json")):
    with open(f, encoding="utf-8") as fp:
        domains.append(json.load(fp))

for f in sorted(DATASET_REGISTRY.glob("*.json")):
    with open(f, encoding="utf-8") as fp:
        datasets.append(json.load(fp))

frozen = [d for d in domains if d.get("freeze", False)]

domain_names = {
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

with open(README, "w", encoding="utf-8") as out:

    out.write("# Global One Health Intelligence Framework (GOHIF)\n\n")

    out.write("## Project Vision\n\n")
    out.write(
        "GOHIF is a reproducible, explainable, evidence-driven computational "
        "framework for integrating heterogeneous One Health evidence to support "
        "antimicrobial resistance surveillance, evidence harmonization, "
        "hypothesis generation, and decision support.\n\n"
    )

    out.write("---\n\n")

    out.write("## Phase 2 Progress\n\n")
    out.write(f"- Frozen Domains: **{len(frozen)} / {len(domains)}**\n")
    out.write(f"- Registered Datasets: **{len(datasets)}**\n\n")

    out.write("### Domain Status\n\n")

    order = [
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

    registry = {d["id"]: d for d in domains}

    for key in order:
        d = registry.get(key)
        if d is None:
            continue

        icon = "✅" if d.get("freeze", False) else "⏳"

        out.write(
            f"- {icon} **{domain_names.get(key,key)}** "
            f"({d['status']})\n"
        )

    out.write("\n---\n\n")

    out.write("## Repository Architecture\n\n")

    out.write("```\n")
    out.write("data/registry/          Dataset registry\n")
    out.write("docs/domain_registry/   Domain registry\n")
    out.write("docs/MRD/              Research documentation\n")
    out.write("docs/MDD/              Development documentation\n")
    out.write("scripts/sync/          Synchronization engine\n")
    out.write("build/phase2/          Generated artifacts\n")
    out.write("```\n\n")

    out.write("---\n\n")

    out.write("## Synchronization\n\n")

    out.write("Regenerate all master documentation using:\n\n")
    out.write("```bash\n")
    out.write("python3 scripts/sync/sync_phase2.py\n")
    out.write("```\n\n")

    out.write("---\n\n")

    out.write("## Current Status\n\n")

    out.write("The project currently uses:\n\n")

    out.write("- Dataset Registry\n")
    out.write("- Domain Registry\n")
    out.write("- Automated Master Dataset Inventory\n")
    out.write("- Automated Master Research Document\n")
    out.write("- Automated Master Development Document\n")
    out.write("- Synchronization Engine\n")

print(f"[OK] Generated {README}")
