from pathlib import Path
import json

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")

CANONICAL = {

    # ---------------- Pathogens ----------------

    "E.coli":"Escherichia coli",
    "E. coli":"Escherichia coli",
    "E.\ncoli":"Escherichia coli",

    "SARS CoV-2":"SARS-CoV-2",
    "SARS-CoV2":"SARS-CoV-2",
    "SARs-CoV-2":"SARS-CoV-2",

    "Influenza":"Influenza virus",
    "influenza":"Influenza virus",

    # ---------------- Diseases ----------------

    "cancer":"Cancer",
    "influenza":"Influenza",
    "malaria":"Malaria",
    "tuberculosis":"Tuberculosis",

}

FIELDS = [
    "genes",
    "proteins",
    "species",
    "diseases",
    "pathogens",
    "countries",
]

count = 0

for file in sorted(ARTIFACTS.glob("*.json")):

    with open(file,encoding="utf-8") as f:
        art=json.load(f)

    for field in FIELDS:

        values=[]

        for item in art["entities"].get(field,[]):

            values.append(
                CANONICAL.get(item,item)
            )

        art["entities"][field]=sorted(set(values))

    with open(file,"w",encoding="utf-8") as f:
        json.dump(art,f,indent=2)

    count+=1

print("="*70)
print("Entity Normalization Complete")
print("="*70)
print("Artifacts Updated:",count)
print("="*70)
