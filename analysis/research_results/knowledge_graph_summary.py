import pandas as pd
from pathlib import Path

BASE = Path("processed/knowledge_graph")

nodes = pd.read_csv(BASE/"nodes.csv")
edges = pd.read_csv(BASE/"edges.csv")

print("="*80)
print("GOHIF KNOWLEDGE GRAPH SUMMARY")
print("="*80)

print(f"Nodes : {len(nodes):,}")
print(f"Edges : {len(edges):,}")

print("\nNODE COLUMNS")
print(nodes.columns.tolist())

print("\nEDGE COLUMNS")
print(edges.columns.tolist())

print("\nFIRST 20 NODES")
print(nodes.head(20).to_string(index=False))

print("\nFIRST 20 EDGES")
print(edges.head(20).to_string(index=False))

nodes.to_csv(
    "analysis/research_results/kg_nodes_copy.csv",
    index=False
)

edges.to_csv(
    "analysis/research_results/kg_edges_copy.csv",
    index=False
)
