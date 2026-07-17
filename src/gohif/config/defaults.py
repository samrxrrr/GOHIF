"""
GOHIF default configuration values.

Every subsystem should obtain default values from this module rather than
hard-coding constants.
"""

from __future__ import annotations

DEFAULT_PROJECT_NAME = "GOHIF"

DEFAULT_VERSION = "0.1.0"

DEFAULT_AUTHOR = "GOHIF Consortium"

DEFAULT_LOG_LEVEL = "INFO"

DEFAULT_LOG_DIRECTORY = "logs"

DEFAULT_DATA_DIRECTORY = "data"

DEFAULT_OUTPUT_DIRECTORY = "results"

DEFAULT_DATABASE = "duckdb"

DEFAULT_DATABASE_FILE = "gohif.duckdb"

DEFAULT_RANDOM_SEED = 42

DEFAULT_THREADS = 4

DEFAULT_ENVIRONMENT = "development"

SUPPORTED_ENVIRONMENTS = (
    "development",
    "testing",
    "production",
)
