import pandas as pd

df = pd.read_csv(
    "analysis/admet/final_gohif_drug_scores.csv"
)

summary = pd.DataFrame({
    "Metric":[
        "Total drug candidates",
        "Unique pathogens",
        "Top GOHIF score",
        "Mean GOHIF score",
        "Median GOHIF score",
        "High confidence candidates (>50)"
    ],
    "Value":[
        len(df),
        df["pathogen"].nunique(),
        round(df["GOHIF_final_score_v3"].max(),3),
        round(df["GOHIF_final_score_v3"].mean(),3),
        round(df["GOHIF_final_score_v3"].median(),3),
        int((df["GOHIF_final_score_v3"]>50).sum())
    ]
})

summary.to_csv(
"analysis/validation/benchmark_summary.csv",
index=False
)

print("="*80)
print("GOHIF BENCHMARK SUMMARY")
print("="*80)
print(summary.to_string(index=False))
