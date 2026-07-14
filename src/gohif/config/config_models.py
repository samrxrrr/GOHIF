"""
GOHIF Configuration Models
==========================

Project:
    Global One Health Intelligence Framework (GOHIF)

Module:
    gohif.config.config_models

Purpose:
    Immutable configuration models used throughout GOHIF.

Version:
    0.2.0
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator

from .constants import (
    CONFIG_ROOT,
    DEFAULT_ENVIRONMENT_NAME,
    DEFAULT_LOG_FILE,
    DEFAULT_LOG_LEVEL,
    PROJECT_CONFIGURATION_FILE,
)


class RuntimeConfiguration(BaseModel):
    """
    Runtime configuration.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    environment_name: str = DEFAULT_ENVIRONMENT_NAME
    debug: bool = False
    workers: int = Field(default=1, ge=1)


class ProjectPaths(BaseModel):
    """
    Canonical project paths.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    project_root: Path
    config_root: Path = CONFIG_ROOT
    datasets: Path
    logs: Path
    reports: Path
    results: Path
    figures: Path
    tables: Path
    workflow: Path

    @field_validator(
        "project_root",
        "config_root",
        "datasets",
        "logs",
        "reports",
        "results",
        "figures",
        "tables",
        "workflow",
        mode="before",
    )
    @classmethod
    def resolve_path(cls, value: str | Path) -> Path:
        return Path(value).expanduser().resolve()


class LoggingConfiguration(BaseModel):
    """
    Logging configuration.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    level: str = DEFAULT_LOG_LEVEL
    filename: str = DEFAULT_LOG_FILE
    console: bool = True

    @field_validator("level")
    @classmethod
    def validate_level(cls, value: str) -> str:
        value = value.upper()

        allowed = {
            "CRITICAL",
            "ERROR",
            "WARNING",
            "INFO",
            "DEBUG",
        }

        if value not in allowed:
            raise ValueError(f"Unsupported log level: {value}")

        return value


class GOHIFConfiguration(BaseModel):
    """
    Root GOHIF configuration model.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    configuration_file: str = PROJECT_CONFIGURATION_FILE

    runtime: RuntimeConfiguration

    paths: ProjectPaths

    logging: LoggingConfiguration = Field(default_factory=LoggingConfiguration)

    metadata: dict[str, str] = Field(default_factory=dict)
