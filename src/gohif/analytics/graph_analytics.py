from pathlib import Path
import csv
import json
from collections import Counter

KG = Path("processed/knowledge_graph")

nodes = []
edges = []

with open(KG/"nodes.csv", encoding="utf-8") as f:
    nodes = list(csv.DictReader(f))

with open(KG/"edges.csv", encoding="utf-8") as f:
    edges = list(csv.DictReader(f))

node_types = Counter(n["type"] for n in nodes)
edge_types = Counter(e["relationship"] for e in edges)

degree = Counter()

for e in edges:
    degree[e["source"]] += 1
    degree[e["target"]] += 1

top_nodes = degree.most_common(20)

report = {

    "total_nodes": len(nodes),

    "total_edges": len(edges),

    "node_types": dict(node_types),

    "edge_types": dict(edge_types),

    "top_connected_nodes": top_nodes

}

with open(KG/"analytics.json","w",encoding="utf-8") as f:
    json.dump(report,f,indent=2)

print("="*70)
print("GOHIF Graph Analytics Complete")
print("="*70)
print(json.dumps(report,indent=2))
print("="*70)
