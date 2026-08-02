from pathlib import Path
import csv
import json

from src.gohif.metadata.extractors.generic_extractor import GenericExtractor
from src.gohif.metadata.extractors.csv_extractor import CSVExtractor

ROOT = Path("/mnt/g/My Drive/DATASETS")

CATALOG = ROOT / "_registry" / "dataset_catalog.csv"

OUTPUT_DIR = ROOT / "_metadata"
OUTPUT_DIR.mkdir(exist_ok=True)


def choose_extractor(path: Path):
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return CSVExtractor()

    return GenericExtractor()


with open(CATALOG, newline="", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        dataset_id = row["dataset_id"]

        dataset_path = ROOT / row["dataset_path"]

        metadata = {
            "dataset_id": dataset_id,
            "dataset_name": row["dataset_name"],
            "domain": row["domain"],
            "dataset_type": row["dataset_type"],
            "dataset_path": str(dataset_path),
            "files": []
        }

        if dataset_path.is_file():

            extractor = choose_extractor(dataset_path)

            metadata["files"].append(
                extractor.extract(dataset_path)
            )

        elif dataset_path.is_dir():

            for file in dataset_path.rglob("*"):

                if not file.is_file():
                    continue

                if file.name.lower() == "desktop.ini":
                    continue

                if ".git" in file.parts:
                    continue

                extractor = choose_extractor(file)

                try:
                    metadata["files"].append(
                        extractor.extract(file)
                    )
                except Exception as e:
                    metadata["files"].append(
                        {
                            "file": str(file),
                            "error": str(e)
                        }
                    )

        out = OUTPUT_DIR / f"{dataset_id}.json"

        with open(out, "w", encoding="utf-8") as fp:
            json.dump(metadata, fp, indent=2)

        print(f"Finished {dataset_id}")
