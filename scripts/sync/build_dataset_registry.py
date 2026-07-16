from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "registry" / "datasets"

OUT.mkdir(parents=True, exist_ok=True)

DATASETS = [

# ---------------------------
# HUMAN HEALTH
# ---------------------------

{
"id":"HH-001",
"name":"WHO GLASS",
"domain":"Human Health",
"organization":"World Health Organization",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"HH-002",
"name":"ATLAS",
"domain":"Human Health",
"organization":"Pfizer",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"HH-003",
"name":"ResistanceMap",
"domain":"Human Health",
"organization":"CDDEP",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"HH-004",
"name":"EARS-Net",
"domain":"Human Health",
"organization":"ECDC",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"HH-005",
"name":"NARMS Human",
"domain":"Human Health",
"organization":"CDC",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"HH-006",
"name":"CAESAR",
"domain":"Human Health",
"organization":"WHO Europe",
"tier":"Tier 2",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"HH-007",
"name":"ReLAVRA+",
"domain":"Human Health",
"organization":"PAHO",
"tier":"Tier 2",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"HH-008",
"name":"GLASS-AMC",
"domain":"Human Health",
"organization":"World Health Organization",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

# ---------------------------
# ANIMAL HEALTH
# ---------------------------

{
"id":"AH-001",
"name":"WOAH WAHIS",
"domain":"Animal Health",
"organization":"WOAH",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"AH-002",
"name":"ANIMUSE",
"domain":"Animal Health",
"organization":"WOAH",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"AH-003",
"name":"ESVAC",
"domain":"Animal Health",
"organization":"EMA",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"AH-004",
"name":"Vet-LIRN",
"domain":"Animal Health",
"organization":"US FDA",
"tier":"Tier 2",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"AH-005",
"name":"DANMAP Animal",
"domain":"Animal Health",
"organization":"Denmark",
"tier":"Tier 2",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"AH-006",
"name":"NARMS Animal",
"domain":"Animal Health",
"organization":"USDA",
"tier":"Tier 2",
"evidence_class":"Primary",
"status":"Accepted"
},

# ---------------------------
# ENVIRONMENTAL HEALTH
# ---------------------------

{
"id":"EH-001",
"name":"WHO Tricycle Environmental Component",
"domain":"Environmental Health",
"organization":"World Health Organization",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"EH-002",
"name":"MGnify",
"domain":"Environmental Health",
"organization":"EMBL-EBI",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"EH-003",
"name":"UNEP GEMS/Water",
"domain":"Environmental Health",
"organization":"UNEP",
"tier":"Tier 1",
"evidence_class":"Contextual",
"status":"Accepted"
},

{
"id":"EH-004",
"name":"Earth Microbiome Project",
"domain":"Environmental Health",
"organization":"EMP Consortium",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"EH-005",
"name":"NORMAN Network",
"domain":"Environmental Health",
"organization":"NORMAN Association",
"tier":"Tier 1",
"evidence_class":"Contextual",
"status":"Accepted"
},

{
"id":"EH-006",
"name":"Curated Wastewater Treatment Evidence Collection",
"domain":"Environmental Health",
"organization":"GOHIF",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

# ---------------------------
# FOOD CHAIN
# ---------------------------

{
"id":"FC-001",
"name":"NARMS Retail Meat Surveillance",
"domain":"Food Chain",
"organization":"CDC/FDA/USDA",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"FC-002",
"name":"EFSA/ECDC Food Component",
"domain":"Food Chain",
"organization":"EFSA/ECDC",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"FC-003",
"name":"CIPARS Food Component",
"domain":"Food Chain",
"organization":"Public Health Agency of Canada",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
},

{
"id":"FC-004",
"name":"GenomeTrakr",
"domain":"Food Chain",
"organization":"US FDA",
"tier":"Tier 1",
"evidence_class":"Primary",
"status":"Accepted"
}

]

count = 0

for ds in DATASETS:
    outfile = OUT / f"{ds['id']}.json"
    with open(outfile,"w",encoding="utf-8") as f:
        json.dump(ds,f,indent=2)
    count += 1

print(f"Created {count} dataset registry files.")
