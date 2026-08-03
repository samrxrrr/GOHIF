import pandas as pd

# Small-molecule prioritization
drug = pd.read_csv(
    "analysis/admet/final_gohif_drug_scores.csv"
)

# Protein prioritization
prot = pd.read_csv(
    "analysis/large_scale/prioritization/prioritized_targets.csv"
)

# Structure coverage
struct = pd.read_csv(
    "analysis/phase44_structure/structure_coverage_dataset.csv"
)

benchmark = pd.DataFrame({

"Metric":[
"Drug candidates",
"Prioritized proteins",
"Experimental structures",
"AlphaFold candidates",
"Mean GOHIF drug score",
"Maximum GOHIF drug score",
"Mean protein priority score",
"Maximum protein priority score"
],

"Value":[
len(drug),
len(prot),
(struct["structure_status"]=="Experimental (PDB)").sum(),
(struct["structure_status"]=="AlphaFold Candidate").sum(),
round(drug["GOHIF_final_score_v3"].mean(),2),
round(drug["GOHIF_final_score_v3"].max(),2),
round(prot["GOHIF_priority_score"].mean(),2),
round(prot["GOHIF_priority_score"].max(),2)

]

})

benchmark.to_csv(
"analysis/phase45_benchmark/gohif_benchmark_summary.csv",
index=False
)

print("="*80)
print("GOHIF INTEGRATED BENCHMARK COMPLETE")
print("="*80)
print()
print(benchmark.to_string(index=False))
