import pandas as pd
from pathlib import Path

OUT = Path("analysis/phase46_tvi")
OUT.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Load protein prioritization
# -----------------------------
prot = pd.read_csv(
    "analysis/large_scale/prioritization/prioritized_targets.csv"
)

# -----------------------------
# Load structure coverage
# -----------------------------
coverage = pd.read_csv(
    "analysis/phase44_structure/structure_coverage.csv"
)

# -----------------------------
# Load drug scores
# -----------------------------
drug = pd.read_csv(
    "analysis/admet/final_gohif_drug_scores.csv"
)

# -----------------------------
# Structure score
# -----------------------------
coverage["structure_score"] = coverage["structure_status"].map({
    "Experimental (PDB)": 1.0,
    "AlphaFold Candidate": 0.7
}).fillna(0.0)

# -----------------------------
# Merge
# -----------------------------
df = prot.merge(
    coverage[["accession", "structure_score"]],
    on="accession",
    how="left"
)

df["structure_score"] = df["structure_score"].fillna(0)

# -----------------------------
# Normalize protein priority
# -----------------------------
mx = df["GOHIF_priority_score"].max()

df["priority_norm"] = (
    df["GOHIF_priority_score"] / mx
)

# -----------------------------
# Global drug evidence
# -----------------------------
drug_score = (
    drug["GOHIF_final_score_v3"].mean()
    / drug["GOHIF_final_score_v3"].max()
)

# -----------------------------
# Therapeutic Vulnerability Index
# -----------------------------
df["TVI"] = (
      0.60 * df["priority_norm"]
    + 0.30 * df["structure_score"]
    + 0.10 * drug_score
)

df = df.sort_values(
    "TVI",
    ascending=False
)

df.to_csv(
    OUT / "therapeutic_vulnerability_index.csv",
    index=False
)

top = df.head(30)

print("="*80)
print("GOHIF THERAPEUTIC VULNERABILITY INDEX")
print("="*80)
print()
print("Proteins:", len(df))
print()
print(top[[
    "normalized_gene",
    "accession",
    "drug_class",
    "GOHIF_priority_score",
    "structure_score",
    "TVI"
]].to_string(index=False))
