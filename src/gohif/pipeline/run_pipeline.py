import subprocess
import time

STEPS = [

    ("Catalog", "gohif.manifest.dataset_catalog_builder"),
    ("Metadata", "gohif.metadata.core.manager"),
    ("Quality Control", "gohif.validation.dataset_validator"),
    ("Standardization", "gohif.standardization.mapper"),
    ("Harmonization", "gohif.harmonization.manager"),
    ("Semantic", "gohif.semantic.entity_extractor"),
    ("Artifacts", "gohif.artifacts.content_builder"),
    ("NER", "gohif.ner.entity_engine"),
    ("Knowledge Graph", "gohif.kg.graph_builder"),
    ("Analytics", "gohif.analytics.graph_analytics"),
    ("Search", "gohif.search.search_engine"),
    ("Similarity", "gohif.similarity.dataset_similarity"),
    ("Association", "gohif.association.cross_domain"),
    ("Evidence", "gohif.evidence.evidence_network"),
    ("Discovery", "gohif.discovery.candidate_discovery"),
    ("Ranking", "gohif.ranking.hotspot_ranker"),
    ("Health", "gohif.health.dataset_health_scanner"),
    ("Repair", "gohif.repair.dataset_repair"),
    ("Provenance", "gohif.provenance.lineage"),
    ("Master Index", "gohif.index.master_index"),
]

print("="*80)
print("GOHIF MASTER PIPELINE")
print("="*80)

start = time.time()

for name, module in STEPS:

    print(f"\n>>> {name}")

    result = subprocess.run(
        ["python", "-m", module]
    )

    if result.returncode != 0:
        print(f"FAILED : {name}")
        break

elapsed = time.time() - start

print("\n" + "="*80)
print("Pipeline Finished")
print(f"Elapsed : {elapsed:.2f} seconds")
print("="*80)
