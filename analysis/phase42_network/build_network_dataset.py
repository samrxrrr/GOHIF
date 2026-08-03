import pandas as pd

df=pd.read_csv(
"analysis/large_scale/prioritization/prioritized_targets.csv"
)

network=df[[
"normalized_gene",
"accession",
"drug_class"
]].copy()

network=network.rename(columns={
"normalized_gene":"source",
"drug_class":"target"
})

network["edge_type"]="confers_resistance_to"

network.to_csv(
"analysis/phase42_network/network_edges.csv",
index=False
)

nodes1=pd.DataFrame({
"id":network["source"],
"type":"protein"
})

nodes2=pd.DataFrame({
"id":network["target"],
"type":"drug_class"
})

nodes=pd.concat([nodes1,nodes2]).drop_duplicates()

nodes.to_csv(
"analysis/phase42_network/network_nodes.csv",
index=False
)

print("="*80)
print("GOHIF NETWORK DATASET CREATED")
print("="*80)

print()

print("Protein nodes :",len(nodes1))
print("Drug classes  :",network["target"].nunique())
print("Total nodes   :",len(nodes))
print("Edges         :",len(network))

print()

print(network.head(20).to_string(index=False))
