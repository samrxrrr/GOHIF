import pandas as pd
from pathlib import Path

# -----------------------------
# Load GOHIF outputs
# -----------------------------

drug = pd.read_csv(
    "analysis/drug_discovery/final_ranking/drug_candidates_v2.csv"
)

# -----------------------------
# Confidence scoring
# -----------------------------

def confidence(score):
    if score >= 40:
        return "Very High"
    elif score >= 25:
        return "High"
    elif score >= 15:
        return "Moderate"
    else:
        return "Low"


drug["confidence"] = drug["GOHIF_drug_score_v2"].apply(confidence)

# -----------------------------
# Therapeutic recommendation
# -----------------------------

recommendations = []

for _, row in drug.iterrows():

    reasons = []

    if row["binding_affinity_kcal_mol"] <= -5:
        reasons.append("Strong docking affinity")

    elif row["binding_affinity_kcal_mol"] <= -4:
        reasons.append("Moderate docking affinity")

    if row["GOHIF_AMR_score"] >= 50:
        reasons.append("High AMR priority")

    elif row["GOHIF_AMR_score"] >= 20:
        reasons.append("Relevant AMR target")

    if row.get("interaction_count",0) >= 5:
        reasons.append("Multiple protein-ligand interactions")

    recommendations.append("; ".join(reasons))

drug["GOHIF_recommendation"] = recommendations

# -----------------------------
# Rank candidates
# -----------------------------

drug = drug.sort_values(
    "GOHIF_drug_score_v2",
    ascending=False
)

drug.insert(
    0,
    "GOHIF_rank",
    range(1,len(drug)+1)
)

# -----------------------------
# Save CSV
# -----------------------------

csv_file = Path(
    "analysis/reports/therapeutic_intelligence_report.csv"
)

drug.to_csv(
    csv_file,
    index=False
)

# -----------------------------
# Text summary
# -----------------------------

summary = []

summary.append("="*80)
summary.append("GOHIF THERAPEUTIC INTELLIGENCE REPORT")
summary.append("="*80)
summary.append("")

summary.append(f"Total therapeutic candidates: {len(drug)}")
summary.append("")

summary.append("TOP 10 CANDIDATES")
summary.append("-"*80)

for _, r in drug.head(10).iterrows():

    summary.append(
        f"""
Rank: {r['GOHIF_rank']}
Pathogen: {r['pathogen']}
Compound: {r['compound']}
Docking affinity: {r['binding_affinity_kcal_mol']} kcal/mol
GOHIF Score: {r['GOHIF_drug_score_v2']:.3f}
Confidence: {r['confidence']}
Recommendation:
{r['GOHIF_recommendation']}
"""
    )

txt_file = Path(
    "analysis/reports/therapeutic_summary.txt"
)

txt_file.write_text(
    "\n".join(summary)
)

print("="*80)
print("GOHIF THERAPEUTIC INTELLIGENCE REPORT COMPLETE")
print("="*80)

print(drug[
[
"GOHIF_rank",
"pathogen",
"compound",
"GOHIF_drug_score_v2",
"confidence"
]
].head(10).to_string(index=False))

print("\nSaved:")
print(csv_file)
print(txt_file)

