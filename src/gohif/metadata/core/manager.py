from pathlib import Path
from datetime import datetime
import csv
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[4]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gohif.metadata.extractors.generic_extractor import GenericExtractor
from gohif.metadata.extractors.csv_extractor import CSVExtractor
from gohif.utils.logging.logger import get_logger
from gohif.manifest.processing_manifest import ProcessingManifest


class MetadataManager:

    def __init__(self):

        self.logger = get_logger("metadata")

        self.root = Path("/mnt/g/My Drive/DATASETS")

        self.catalog = self.root / "_registry" / "dataset_catalog.csv"

        self.output_dir = self.root / "_metadata"

        self.output_dir.mkdir(exist_ok=True)

        self.manifest = ProcessingManifest(
            self.output_dir / "processing_manifest.json"
        )

        self.processed = 0
        self.failed = 0
        self.skipped = 0

    def choose_extractor(self, path):

        if path.suffix.lower() == ".csv":
            return CSVExtractor()

        return GenericExtractor()

    def process_file(self, file):

        extractor = self.choose_extractor(file)

        try:

            return extractor.extract(file)

        except Exception as e:

            self.failed += 1

            self.logger.exception(
                "Failed extracting %s",
                file,
            )

            return {
                "file": str(file),
                "error": str(e),
            }

    def process_dataset(self, row):

        dataset_id = row["dataset_id"]

        if self.manifest.is_completed(dataset_id):

            self.skipped += 1

            self.logger.info(
                "Skipping %s (already processed)",
                dataset_id,
            )

            return

        dataset_path = self.root / row["dataset_path"]

        metadata = {
            "dataset_id": dataset_id,
            "dataset_name": row["dataset_name"],
            "domain": row["domain"],
            "dataset_type": row["dataset_type"],
            "dataset_path": str(dataset_path),
            "files": [],
        }

        self.logger.info(
            "Processing %s",
            dataset_id,
        )

        if dataset_path.is_file():

            metadata["files"].append(
                self.process_file(dataset_path)
            )

        elif dataset_path.is_dir():

            for file in dataset_path.rglob("*"):

                if not file.is_file():
                    continue

                if file.name.lower() == "desktop.ini":
                    continue

                if ".git" in file.parts:
                    continue

                metadata["files"].append(
                    self.process_file(file)
                )

        out = self.output_dir / f"{dataset_id}.json"

        with open(out, "w", encoding="utf-8") as fp:

            json.dump(
                metadata,
                fp,
                indent=2,
            )

        self.manifest.mark_completed(dataset_id)

        self.processed += 1

        self.logger.info(
            "Finished %s",
            dataset_id,
        )

    def run(self):

        self.logger.info("=" * 80)
        self.logger.info("GOHIF Metadata Generation Started")
        self.logger.info("=" * 80)

        with open(self.catalog, newline="", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            for row in reader:

                self.process_dataset(row)

        self.logger.info("=" * 80)
        self.logger.info("Metadata Generation Completed")
        self.logger.info("Processed : %d", self.processed)
        self.logger.info("Skipped   : %d", self.skipped)
        self.logger.info("Failed    : %d", self.failed)
        self.logger.info("=" * 80)


if __name__ == "__main__":

    MetadataManager().run()
