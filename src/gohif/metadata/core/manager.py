from pathlib import Path
import csv
import json

from src.gohif.metadata.extractors.csv_extractor import CSVExtractor
from src.gohif.metadata.extractors.generic_extractor import GenericExtractor

ROOT = Path("/mnt/g/My Drive/DATASETS")
MANIFEST = ROOT / "_registry" / "dataset_manifest.csv"
OUTPUT = ROOT / "_metadata"

OUTPUT.mkdir(exist_ok=True)

extractors = [

    CSVExtractor(),

    GenericExtractor(),

]

with open(MANIFEST, newline="", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        folder = ROOT / row["primary_path"]

        metadata = []

        for file in folder.rglob("*"):

            if not file.is_file():
                continue

            for ext in extractors:

                if ext.supports(str(file)):

                    metadata.append(ext.extract(file))

                    break

        outfile = OUTPUT / f'{row["dataset_id"]}.json'

        with open(outfile, "w", encoding="utf-8") as out:

            json.dump({

                "dataset_id": row["dataset_id"],

                "dataset_name": row["dataset_name"],

                "domain": row["domain"],

                "files": metadata

            }, out, indent=2)

        print("Finished", row["dataset_id"])
