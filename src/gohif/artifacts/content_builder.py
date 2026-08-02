from pathlib import Path
import json

from gohif.extraction.pdf_extractor import PDFExtractor

ARTIFACTS = Path("/mnt/g/My Drive/DATASETS/_artifacts")

pdf = PDFExtractor()

count = 0

for file in sorted(ARTIFACTS.glob("*.json")):

    with open(file,encoding="utf-8") as f:

        artifact = json.load(f)

    source = Path("/mnt/g/My Drive/DATASETS") / artifact["source_file"]

    if source.suffix.lower() != ".pdf":
        continue

    content = pdf.extract(source)

    artifact["content"] = content

    with open(file,"w",encoding="utf-8") as f:

        json.dump(artifact,f,indent=2)

    count += 1

print("="*70)
print("PDF Artifacts Processed :",count)
print("="*70)
