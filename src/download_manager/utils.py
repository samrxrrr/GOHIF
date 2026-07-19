from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------

LOG_DIR = Path("logs/downloads")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "download_manager.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("GOHIF")


# ---------------------------------------------------------------------
# Directory Utilities
# ---------------------------------------------------------------------

def ensure_directory(path: str | Path) -> Path:
    """
    Create a directory if it does not already exist.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


# ---------------------------------------------------------------------
# File Utilities
# ---------------------------------------------------------------------

def verify_file(filepath: str | Path) -> bool:
    """
    Check whether a file exists and is not empty.
    """
    filepath = Path(filepath)
    return filepath.exists() and filepath.is_file() and filepath.stat().st_size > 0


def file_size_mb(filepath: str | Path) -> float:
    """
    Return file size in MB.
    """
    filepath = Path(filepath)
    return round(filepath.stat().st_size / (1024 * 1024), 2)


def sha256sum(filepath: str | Path) -> str:
    """
    Compute SHA-256 checksum.
    """
    filepath = Path(filepath)

    h = hashlib.sha256()

    with filepath.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


# ---------------------------------------------------------------------
# Time Utilities
# ---------------------------------------------------------------------

def timestamp() -> str:
    """
    Current timestamp.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------------------
# Logging Helpers
# ---------------------------------------------------------------------

def log_download(dataset: str, status: str, message: str = "") -> None:
    """
    Log a download event.
    """
    logger.info("%s | %s | %s", dataset, status, message)


# ---------------------------------------------------------------------
# Test Runner
# ---------------------------------------------------------------------

if __name__ == "__main__":
    print("Timestamp :", timestamp())

    ensure_directory("tmp/test")

    print("Directory :", Path("tmp/test").exists())

    print("Verify tmp:", verify_file("tmp"))

    print("Logger OK")

    log_download(
        dataset="TEST",
        status="SUCCESS",
        message="Download manager initialized."
    )

    print("Initialization complete.")
