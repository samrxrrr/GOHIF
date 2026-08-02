"""
GOHIF Corpus Builder
Builds a unified textual corpus from artifact JSON files.
"""

from pathlib import Path
import json

ARTIFACT_DIR = Path("/mnt/g/My Drive/DATASETS/_artifacts")
OUTPUT_FILE = Path("processed/corpus/corpus.jsonl")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

count = 0

with OUTPUT_FILE.open("w", encoding="utf-8") as out:

    for file in sorted(ARTIFACT_DIR.glob("*.json")):

        try:
            obj = json.loads(file.read_text(encoding="utf-8"))

            dataset = obj.get("dataset_id","")

            title = obj.get("title","")

            content = obj.get("content","")

            if isinstance(content, dict):
                content = json.dumps(content)

            if isinstance(content, list):
                content = " ".join(map(str,content))

            text = f"{title}\n{content}"

            record = {
                "dataset_id": dataset,
                "text": text
            }

            out.write(json.dumps(record, ensure_ascii=False) + "\n")

            count += 1

        except Exception:
            pass

print("="*70)
print("GOHIF Corpus Builder")
print("="*70)
print("Documents:", count)
print("Output:", OUTPUT_FILE)
