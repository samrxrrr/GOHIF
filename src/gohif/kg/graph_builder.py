from pathlib import Path
import json
import csv

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")
OUTPUT = Path("processed/knowledge_graph")

OUTPUT.mkdir(parents=True, exist_ok=True)

nodes = {}
edges = []

def add_node(node_id, node_type, label):
    if node_id not in nodes:
        nodes[node_id] = {
            "id": node_id,
            "type": node_type,
            "label": label
        }

for artifact_file in sorted(ARTIFACTS.glob("*.json")):

    with open(artifact_file, encoding="utf-8") as f:
        art = json.load(f)

    dataset = art["dataset_id"]

    add_node(dataset, "Dataset", dataset)

    provider = art["metadata"].get("provider", "")
    if provider:
        pid = f"provider::{provider}"
        add_node(pid, "Provider", provider)
        edges.append([dataset, "HAS_PROVIDER", pid])

    domain = art["metadata"].get("domain", "")
    if domain:
        did = f"domain::{domain}"
        add_node(did, "Domain", domain)
        edges.append([dataset, "HAS_DOMAIN", did])

    for gene in art["entities"].get("genes", []):
        gid = f"gene::{gene}"
        add_node(gid, "Gene", gene)
        edges.append([dataset, "MENTIONS_GENE", gid])

    for disease in art["entities"].get("diseases", []):
        did = f"disease::{disease}"
        add_node(did, "Disease", disease)
        edges.append([dataset, "MENTIONS_DISEASE", did])

    for pathogen in art["entities"].get("pathogens", []):
        pid = f"pathogen::{pathogen}"
        add_node(pid, "Pathogen", pathogen)
        edges.append([dataset, "MENTIONS_PATHOGEN", pid])

    for species in art["entities"].get("species", []):
        sid = f"species::{species}"
        add_node(sid, "Species", species)
        edges.append([dataset, "MENTIONS_SPECIES", sid])

with open(OUTPUT/"nodes.csv","w",newline="",encoding="utf-8") as f:
    writer=csv.DictWriter(f,fieldnames=["id","type","label"])
    writer.writeheader()
    writer.writerows(nodes.values())

with open(OUTPUT/"edges.csv","w",newline="",encoding="utf-8") as f:
    writer=csv.writer(f)
    writer.writerow(["source","relationship","target"])
    writer.writerows(edges)

summary={
    "nodes":len(nodes),
    "edges":len(edges)
}

with open(OUTPUT/"summary.json","w",encoding="utf-8") as f:
    json.dump(summary,f,indent=2)

print("="*70)
print("GOHIF Knowledge Graph Built")
print("="*70)
print(summary)
print("="*70)
