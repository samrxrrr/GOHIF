from pathlib import Path
from datetime import datetime
import csv
import json
import sys

# ------------------------------------------------------------------
# Add GOHIF project root to Python path
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[4]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.gohif.metadata.extractors.generic_extractor import GenericExtractor
from src.gohif.metadata.extractors.csv_extractor import CSVExtractor
from src.gohif.utils.logging.logger import get_logger

logger = get_logger("metadata")

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
ROOT = Path("/mnt/g/My Drive/DATASETS")

CATALOG = ROOT / "_registry" / "dataset_catalog.csv"

OUTPUT_DIR = ROOT / "_metadata"
OUTPUT_DIR.mkdir(exist_ok=True)

processed = 0
failed = 0

logger.info("=" * 80)
logger.info("GOHIF Metadata Generation Started")
logger.info("Catalog : %s", CATALOG)
logger.info("Output  : %s", OUTPUT_DIR)
logger.info("Started : %s", datetime.now().isoformat())
logger.info("=" * 80)


def choose_extractor(path: Path):
    """
    Return the correct metadata extractor for a file.
    """
    if path.suffix.lower() == ".csv":
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
            "files": [],
        }

        logger.info("Processing %s", dataset_id)

        if dataset_path.is_file():

            extractor = choose_extractor(dataset_path)

            try:

                metadata["files"].append(
                    extractor.extract(dataset_path)
                )

            except Exception as e:

                failed += 1

                logger.exception(
                    "Extraction failed: %s",
                    dataset_path,
                )

                metadata["files"].append(
                    {
                        "file": str(dataset_path),
                        "error": str(e),
                    }
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

                    failed += 1

                    logger.exception(
                        "Extraction failed: %s",
                        file,
                    )

                    metadata["files"].append(
                        {
                            "file": str(file),
                            "error": str(e),
                        }
                    )

        out = OUTPUT_DIR / f"{dataset_id}.json"

        with open(out, "w", encoding="utf-8") as fp:
            json.dump(metadata, fp, indent=2)

        processed += 1

        logger.info(
            "Finished %s (%d files)",
            dataset_id,
            len(metadata["files"]),
        )

logger.info("=" * 80)
logger.info("Metadata Generation Completed")
logger.info("Datasets processed : %d", processed)
logger.info("Extraction errors  : %d", failed)
logger.info("Finished : %s", datetime.now().isoformat())
logger.info("=" * 80)
