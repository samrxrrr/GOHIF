import pandas as pd

edges=pd.read_csv(
"analysis/phase42_network/network_edges.csv"
)

degree=(
edges.groupby("target")
.size()
.sort_values(ascending=False)
.reset_index(name="proteins")
)

degree.to_csv(
"analysis/phase42_network/drug_class_statistics.csv",
index=False
)

print("="*80)
print("GOHIF NETWORK STATISTICS")
print("="*80)

print()

print(degree.to_string(index=False))
