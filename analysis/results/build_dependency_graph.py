from pathlib import Path
import pandas as pd

registry = pd.read_csv(
    "analysis/results/registry/gohif_data_registry.csv"
)

edges = []

for f in registry["file"]:

    parts = Path(f).parts

    if len(parts) >= 2:
        edges.append({
            "module": parts[0],
            "subcategory": parts[1],
            "file": f
        })

pd.DataFrame(edges).to_csv(
    "analysis/results/registry/dependency_graph.csv",
    index=False
)

print("="*80)
print("GOHIF DEPENDENCY GRAPH")
print("="*80)
print(pd.DataFrame(edges).head(30).to_string(index=False))
