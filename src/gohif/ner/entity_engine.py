from pathlib import Path
import json
import re

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")

PATTERNS = {

    "genes": [
        r"\bTP53\b",
        r"\bEGFR\b",
        r"\bBRCA1\b",
        r"\bBRCA2\b",
        r"\bKRAS\b",
        r"\bMYC\b",
        r"\bPTEN\b",
        r"\bTNF\b",
        r"\bIL6\b",
    ],

    "pathogens": [
        r"SARS[- ]?CoV[- ]?2",
        r"Salmonella",
        r"Escherichia coli",
        r"\bE\.?\s*coli\b",
        r"Influenza",
        r"Mycobacterium tuberculosis",
    ],

    "species": [
        r"Homo sapiens",
        r"Mus musculus",
        r"Bos taurus",
        r"Sus scrofa",
        r"Gallus gallus",
    ],

    "diseases": [
        r"COVID[- ]?19",
        r"Tuberculosis",
        r"Influenza",
        r"Cancer",
        r"Malaria",
    ]
}

processed = 0

for artifact_file in sorted(ARTIFACTS.glob("*.json")):

    with open(artifact_file, encoding="utf-8") as f:
        artifact = json.load(f)

    text = artifact.get("content", {}).get("text", "")

    if not text:
        continue

    for category, patterns in PATTERNS.items():

        found = set(artifact["entities"].get(category, []))

        for pattern in patterns:

            for match in re.findall(pattern, text, flags=re.I):

                found.add(match)

        artifact["entities"][category] = sorted(found)

    with open(artifact_file, "w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=2)

    processed += 1

print("=" * 70)
print("Scientific NER Complete")
print("=" * 70)
print("Artifacts processed:", processed)
print("=" * 70)
