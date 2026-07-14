"""
GOHIF Configuration Constants
=============================

Project:
    Global One Health Intelligence Framework (GOHIF)

Module:
    gohif.config.constants

Purpose:
    Defines immutable constants used throughout the GOHIF framework.

Author:
    GOHIF Development Team

Version:
    0.2.0

License:
    Refer to the repository LICENSE file.
"""

from pathlib import Path

###############################################################################
# Project Information
###############################################################################

PROJECT_NAME: str = "Global One Health Intelligence Framework"
PROJECT_SHORT_NAME: str = "GOHIF"

FRAMEWORK_VERSION: str = "0.2.0-dev"

DEFAULT_ENCODING: str = "utf-8"

###############################################################################
# Repository Structure
###############################################################################

REPOSITORY_ROOT_NAME: str = "GOHIF"

CONFIG_DIRECTORY: str = "config"

DATASET_DIRECTORY: str = "datasets"

LOG_DIRECTORY: str = "logs"

REPORT_DIRECTORY: str = "reports"

RESULT_DIRECTORY: str = "results"

FIGURE_DIRECTORY: str = "figures"

TABLE_DIRECTORY: str = "tables"

WORKFLOW_DIRECTORY: str = "workflow"

###############################################################################
# Configuration Files
###############################################################################

PROJECT_CONFIGURATION_FILE: str = "project.yaml"

ANALYSIS_CONFIGURATION_FILE: str = "analysis.yaml"

DATASET_CONFIGURATION_FILE: str = "datasets.yaml"

LOGGING_CONFIGURATION_FILE: str = "logging.yaml"

###############################################################################
# Logging Defaults
###############################################################################

DEFAULT_LOG_LEVEL: str = "INFO"

DEFAULT_LOG_FILE: str = "gohif.log"

###############################################################################
# Supported Configuration Extensions
###############################################################################

SUPPORTED_CONFIGURATION_EXTENSIONS: tuple[str, ...] = (
    ".yaml",
    ".yml",
)

###############################################################################
# Environment
###############################################################################

DEFAULT_ENVIRONMENT_NAME: str = "gohif"

###############################################################################
# Research Object Prefixes
###############################################################################

RO_PREFIX: str = "RO"

WORK_PACKAGE_PREFIX: str = "WP"

TASK_PREFIX: str = "T"

###############################################################################
# Validation
###############################################################################

REQUIRED_CONFIGURATION_FILES: tuple[str, ...] = (
    PROJECT_CONFIGURATION_FILE,
    ANALYSIS_CONFIGURATION_FILE,
    DATASET_CONFIGURATION_FILE,
    LOGGING_CONFIGURATION_FILE,
)

###############################################################################
# Paths
###############################################################################

CURRENT_FILE = Path(__file__).resolve()

PACKAGE_ROOT = CURRENT_FILE.parent

SRC_ROOT = PACKAGE_ROOT.parent

PROJECT_ROOT = SRC_ROOT.parent.parent

CONFIG_ROOT = PROJECT_ROOT / CONFIG_DIRECTORY

###############################################################################
# End of File
###############################################################################
