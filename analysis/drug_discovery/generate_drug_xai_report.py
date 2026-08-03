import pandas as pd


df=pd.read_csv(
"analysis/drug_discovery/final_drug_candidates.csv"
)


df["explanation"]=""


for i,row in df.iterrows():

    reasons=[]

    if row["GOHIF_AMR_score"] > 50:
        reasons.append(
        "High AMR priority target"
        )

    if row["binding_affinity_kcal_mol"] < -5:
        reasons.append(
        "Strong docking affinity"
        )

    elif row["binding_affinity_kcal_mol"] < -4:
        reasons.append(
        "Moderate docking affinity"
        )

    reasons.append(
    "Structure-supported computational screening"
    )


    df.loc[i,"explanation"]="; ".join(reasons)


df.to_csv(
"analysis/drug_discovery/drug_candidate_explanations.csv",
index=False
)


print("="*80)
print("GOHIF EXPLAINABLE DRUG DISCOVERY REPORT COMPLETE")
print("="*80)


print(
df[
[
"pathogen",
"compound",
"GOHIF_final_drug_score",
"explanation"
]
].head(10).to_string(index=False)
)

