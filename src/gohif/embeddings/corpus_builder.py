from pathlib import Path
import json

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")
OUT = Path("processed/corpus/corpus.jsonl")

OUT.parent.mkdir(parents=True, exist_ok=True)

count = 0

with open(OUT, "w", encoding="utf-8") as writer:

    for file in sorted(ARTIFACTS.glob("*.json")):

        try:

            with open(file, encoding="utf-8") as fp:
                obj = json.load(fp)

            meta = obj.get("metadata", {})
            entities = obj.get("entities", {})
            content = obj.get("content", {})

            text = []

            text.append(meta.get("dataset_name", ""))
            text.append(meta.get("title", ""))
            text.append(meta.get("domain", ""))
            text.append(meta.get("provider", ""))

            for value in entities.values():
                if isinstance(value, list):
                    text.extend(str(x) for x in value)

            if isinstance(content, dict):
                text.append(content.get("title", ""))
                text.append(content.get("text", ""))

            elif isinstance(content, str):
                text.append(content)

            record = {
                "dataset_id": obj.get("dataset_id"),
                "text": "\n".join(str(x) for x in text if x)
            }

            writer.write(json.dumps(record, ensure_ascii=False) + "\n")

            count += 1

        except Exception:
            pass

print("=" * 70)
print("GOHIF Corpus Built")
print("=" * 70)
print("Documents :", count)
print("Output :", OUT)
