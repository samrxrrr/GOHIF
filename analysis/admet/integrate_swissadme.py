import pandas as pd

# -----------------------------
# GOHIF candidates
# -----------------------------

drug = pd.read_csv(
    "analysis/drug_discovery/final_ranking/drug_candidates_v2.csv"
)

# Keep one entry per compound
compound_map = (
    drug[["compound"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# -----------------------------
# SwissADME
# -----------------------------

admet = pd.read_csv(
    "analysis/admet/raw/swissadme_results.csv"
)

if len(admet) != len(compound_map):
    print("WARNING:")
    print("Number of SwissADME rows differs from number of compounds.")
    print(len(admet), len(compound_map))

admet.insert(
    0,
    "compound",
    compound_map["compound"]
)

# -----------------------------
# Merge
# -----------------------------

merged = drug.merge(
    admet,
    on="compound",
    how="left"
)

# -----------------------------
# ADMET score
# -----------------------------

score=[]

for _,r in merged.iterrows():

    s=0

    if r["GI absorption"]=="High":
        s+=2

    if r["BBB permeant"]=="No":
        s+=1

    if r["Lipinski #violations"]==0:
        s+=2

    if r["PAINS #alerts"]==0:
        s+=2

    if r["Brenk #alerts"]==0:
        s+=1

    if r["Bioavailability Score"]>=0.55:
        s+=2

    score.append(s)

merged["GOHIF_ADMET_score"]=score

# -----------------------------
# Final GOHIF score v3
# -----------------------------

merged["GOHIF_final_score_v3"]=(
    merged["GOHIF_drug_score_v2"]*0.8
    +
    merged["GOHIF_ADMET_score"]*2
)

merged=merged.sort_values(
    "GOHIF_final_score_v3",
    ascending=False
)

merged.to_csv(
    "analysis/admet/final_gohif_drug_scores.csv",
    index=False
)

print("="*80)
print("GOHIF ADMET INTEGRATION COMPLETE")
print("="*80)

print(
merged[
[
"compound",
"pathogen",
"GOHIF_drug_score_v2",
"GOHIF_ADMET_score",
"GOHIF_final_score_v3"
]
].to_string(index=False)
)

