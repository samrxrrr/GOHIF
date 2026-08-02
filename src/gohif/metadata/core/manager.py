from pathlib import Path
from datetime import datetime
import csv
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[4]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.gohif.metadata.extractors.generic_extractor import GenericExtractor
from src.gohif.metadata.extractors.csv_extractor import CSVExtractor
from src.gohif.utils.logging.logger import get_logger


class MetadataManager:

    def __init__(self):

        self.logger = get_logger("metadata")

        self.root = Path("/mnt/g/My Drive/DATASETS")

        self.catalog = self.root / "_registry" / "dataset_catalog.csv"

        self.output_dir = self.root / "_metadata"

        self.output_dir.mkdir(exist_ok=True)

        self.processed = 0
        self.failed = 0

    def choose_extractor(self, path: Path):

        if path.suffix.lower() == ".csv":
            return CSVExtractor()

        return GenericExtractor()

    def process_file(self, file: Path):

        extractor = self.choose_extractor(file)

        try:

            return extractor.extract(file)

        except Exception as e:

            self.failed += 1

            self.logger.exception(
                "Failed extracting metadata from %s",
                file,
            )

            return {
                "file": str(file),
                "error": str(e),
            }

    def process_dataset(self, row):

        dataset_id = row["dataset_id"]

        dataset_path = self.root / row["dataset_path"]

        metadata = {
            "dataset_id": dataset_id,
            "dataset_name": row["dataset_name"],
            "domain": row["domain"],
            "dataset_type": row["dataset_type"],
            "dataset_path": str(dataset_path),
            "files": [],
        }

        self.logger.info("Processing %s", dataset_id)

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

        self.processed += 1

        self.logger.info(
            "Finished %s (%d files)",
            dataset_id,
            len(metadata["files"]),
        )

    def run(self):

        self.logger.info("=" * 80)
        self.logger.info("GOHIF Metadata Generation Started")
        self.logger.info("Catalog : %s", self.catalog)
        self.logger.info("Output  : %s", self.output_dir)
        self.logger.info("Started : %s", datetime.now().isoformat())
        self.logger.info("=" * 80)

        with open(self.catalog, newline="", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            for row in reader:

                self.process_dataset(row)

        self.logger.info("=" * 80)
        self.logger.info("Metadata Generation Completed")
        self.logger.info(
            "Datasets processed : %d",
            self.processed,
        )
        self.logger.info(
            "Extraction errors  : %d",
            self.failed,
        )
        self.logger.info(
            "Finished : %s",
            datetime.now().isoformat(),
        )
        self.logger.info("=" * 80)


if __name__ == "__main__":

    manager = MetadataManager()

    manager.run()
