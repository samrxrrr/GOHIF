import pandas as pd

reg = pd.read_csv(
    "analysis/results/registry/gohif_data_registry.csv"
)

manifest = {
    "total_files": len(reg),
    "csv_files": (reg["extension"]==".csv").sum(),
    "json_files": (reg["extension"]==".json").sum(),
    "images": reg["extension"].isin([".png",".svg"]).sum(),
    "pickle": (reg["extension"]==".pkl").sum(),
    "documents": reg["extension"].isin(
        [".pdf",".txt",".xlsx"]
    ).sum()
}

pd.DataFrame(
    manifest.items(),
    columns=["Metric","Value"]
).to_csv(
    "metadata/project_manifest.csv",
    index=False
)

print("="*80)
print("GOHIF PROJECT MANIFEST")
print("="*80)

for k,v in manifest.items():
    print(f"{k:20s} {v}")
