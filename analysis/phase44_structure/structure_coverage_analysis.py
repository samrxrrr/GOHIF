import pandas as pd

df=pd.read_csv(
"analysis/large_scale/prioritization/prioritized_targets.csv"
)

df["pdb_count"]=df["pdb_count"].fillna(0)

df["structure_status"]=df["pdb_count"].apply(
lambda x: "Experimental (PDB)" if x>0 else "AlphaFold Candidate"
)

summary=(
df.groupby("structure_status")
.size()
.reset_index(name="Proteins")
)

summary["Percentage"]=(
summary["Proteins"]/len(df)*100
).round(2)

summary.to_csv(
"analysis/phase44_structure/structure_coverage_summary.csv",
index=False
)

df.to_csv(
"analysis/phase44_structure/structure_coverage_dataset.csv",
index=False
)

print("="*80)
print("GOHIF STRUCTURE COVERAGE COMPLETE")
print("="*80)
print(summary.to_string(index=False))
print()
print("Total proteins:",len(df))
