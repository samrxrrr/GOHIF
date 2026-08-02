from pathlib import Path
import json

INPUT = Path("/mnt/g/My Drive/DATASETS/_metadata_harmonized")
OUTPUT = Path("/mnt/g/My Drive/DATASETS/_metadata_semantic")

OUTPUT.mkdir(exist_ok=True)

ENTITY_RULES = {

    "countries": {

        "india":"India",
        "china":"China",
        "usa":"United States",
        "united states":"United States",
        "uk":"United Kingdom",

    },

    "organisms": {

        "human":"Homo sapiens",
        "mouse":"Mus musculus",
        "rat":"Rattus norvegicus",
        "pig":"Sus scrofa",
        "cattle":"Bos taurus",
        "chicken":"Gallus gallus",

    },

    "pathogens": {

        "salmonella":"Salmonella",
        "ecoli":"Escherichia coli",
        "e. coli":"Escherichia coli",
        "influenza":"Influenza virus",
        "sars":"SARS-CoV",
        "covid":"SARS-CoV-2",

    },

    "diseases": {

        "tuberculosis":"Tuberculosis",
        "malaria":"Malaria",
        "covid":"COVID-19",
        "influenza":"Influenza",

    }

}


def extract(text):

    text = text.lower()

    entities = {

        "countries":[],
        "organisms":[],
        "pathogens":[],
        "diseases":[],

    }

    for category in ENTITY_RULES:

        for keyword, value in ENTITY_RULES[category].items():

            if keyword in text:

                entities[category].append(value)

    return entities


count = 0

for file in sorted(INPUT.glob("GOHIF_DS_*.json")):

    with open(file, encoding="utf-8") as f:

        obj = json.load(f)

    text = " ".join([

        obj.get("dataset_name",""),

        obj.get("title",""),

        obj.get("provider",""),

        obj.get("domain",""),

        " ".join(obj.get("keywords",[]))

    ])

    entities = extract(text)

    obj["countries"] = sorted(set(entities["countries"]))
    obj["organisms"] = sorted(set(entities["organisms"]))
    obj["pathogens"] = sorted(set(entities["pathogens"]))
    obj["diseases"] = sorted(set(entities["diseases"]))

    with open(OUTPUT/file.name,"w",encoding="utf-8") as f:

        json.dump(obj,f,indent=2)

    count += 1

print("="*70)
print("GOHIF Semantic Extraction Complete")
print("="*70)
print("Datasets processed :",count)
print("Output :",OUTPUT)
print("="*70)
