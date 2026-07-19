"""
GOHIF Download Logger
Author: GOHIF
"""

import logging
from pathlib import Path

LOG_DIR = Path("logs/downloads")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "download_manager.log"

logger = logging.getLogger("GOHIF")

if not logger.handlers:

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(LOG_FILE)

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


class DownloadLogger:

    @staticmethod
    def info(message):
        logger.info(message)

    @staticmethod
    def warning(message):
        logger.warning(message)

    @staticmethod
    def error(message):
        logger.error(message)

    @staticmethod
    def success(dataset):
        logger.info(f"{dataset} | SUCCESS")

    @staticmethod
    def failed(dataset, error):
        logger.error(f"{dataset} | FAILED | {error}")

    @staticmethod
    def started(dataset):
        logger.info(f"{dataset} | STARTED")


if __name__ == "__main__":

    DownloadLogger.started("TEST")

    DownloadLogger.success("TEST")

    DownloadLogger.failed("TEST", "Example failure")

    print("Logger initialized successfully.")
