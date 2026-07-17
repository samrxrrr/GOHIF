"""
Global constants used throughout GOHIF.
"""

from __future__ import annotations

from pathlib import Path

PROJECT_NAME = "GOHIF"

SUPPORTED_METADATA_FORMATS = (
    "json",
    "yaml",
    "csv",
)

SUPPORTED_DATA_FORMATS = (
    "csv",
    "tsv",
    "parquet",
    "json",
    "xlsx",
)

DEFAULT_ENCODING = "utf-8"

ROOT_PACKAGE = "gohif"

CONFIG_DIRECTORY = Path("config")

DATA_DIRECTORY = Path("data")

LOG_DIRECTORY = Path("logs")

REPORT_DIRECTORY = Path("reports")
