from pathlib import Path

required=[
"analysis/amr_integration/amr_target_rankings.csv",
"analysis/admet/final_gohif_drug_scores.csv",
"analysis/validation/publication_table.csv",
"analysis/biological_annotation/functional_annotations.csv",
"analysis/large_scale/results/master_amr_dataset.csv"
]

print("="*80)
print("GOHIF READINESS CHECK")
print("="*80)

for f in required:

    print(
        f,
        "OK" if Path(f).exists() else "MISSING"
    )
