from pathlib import Path
import json

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")

datasets = []

for file in sorted(ARTIFACTS.glob("*.json")):
    with open(file, encoding="utf-8") as f:
        datasets.append(json.load(f))

print("="*72)
print("GOHIF DATASET EXPLORER")
print("="*72)

while True:

    dataset = input("\nDataset ID (or exit): ").strip()

    if dataset.lower() == "exit":
        break

    found = False

    for obj in datasets:

        if obj["dataset_id"] != dataset:
            continue

        found = True

        print("\n" + "="*72)

        print("Dataset ID   :", obj["dataset_id"])
        print("Name         :", obj["metadata"].get("dataset_name"))
        print("Domain       :", obj["metadata"].get("domain"))
        print("Provider     :", obj["metadata"].get("provider"))
        print("Type         :", obj["metadata"].get("dataset_type"))
        print("Path         :", obj["metadata"].get("dataset_path"))

        print("\n----- ENTITIES -----")

        for field in [
            "genes",
            "proteins",
            "species",
            "diseases",
            "pathogens",
            "countries"
        ]:

            values = obj["entities"].get(field, [])

            if values:
                print(f"{field:12}: {', '.join(values)}")

        print("\n----- CONTENT -----")

        content = obj.get("content", {})

        title = content.get("title", "")

        if title:
            print("Title :", title)

        text = content.get("text", "")

        if text:
            print("\nPreview\n")
            print(text[:1200])

        break

    if not found:
        print("Dataset not found.")

print("\nExplorer closed.")
