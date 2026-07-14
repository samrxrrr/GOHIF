"""
GOHIF Configuration Loader
==========================

Project:
    Global One Health Intelligence Framework (GOHIF)

Module:
    gohif.config.config_loader

Purpose:
    Load GOHIF configuration files into immutable configuration models.

Version:
    0.2.0
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .config_models import GOHIFConfiguration
from .config_models import ProjectPaths
from .config_models import RuntimeConfiguration
from .constants import (
    CONFIG_ROOT,
    FIGURE_DIRECTORY,
    LOG_DIRECTORY,
    PROJECT_CONFIGURATION_FILE,
    PROJECT_ROOT,
    REPORT_DIRECTORY,
    RESULT_DIRECTORY,
    TABLE_DIRECTORY,
    WORKFLOW_DIRECTORY,
    DATASET_DIRECTORY,
)
from .exceptions import ConfigurationError


class ConfigurationLoader:
    """
    Loads GOHIF project configuration from YAML.
    """

    def __init__(self, config_directory: Path | str = CONFIG_ROOT) -> None:
        self._config_directory = Path(config_directory).expanduser().resolve()

    @property
    def config_directory(self) -> Path:
        return self._config_directory

    @property
    def configuration_file(self) -> Path:
        return self._config_directory / PROJECT_CONFIGURATION_FILE

    def exists(self) -> bool:
        return self.configuration_file.exists()

    def load(self) -> GOHIFConfiguration:
        """
        Load the project configuration.

        Returns
        -------
        GOHIFConfiguration
            Immutable configuration object.

        Raises
        ------
        ConfigurationError
            If configuration cannot be loaded.
        """

        data = self._read_yaml()

        runtime = RuntimeConfiguration(**data.get("runtime", {}))

        paths = self._build_paths(data.get("paths", {}))

        metadata = data.get("metadata", {})

        return GOHIFConfiguration(
            runtime=runtime,
            paths=paths,
            metadata=metadata,
        )

    def _read_yaml(self) -> dict[str, Any]:
        if not self.exists():
            raise ConfigurationError(
                f"Configuration file not found: {self.configuration_file}"
            )

        try:
            with self.configuration_file.open(
                "r",
                encoding="utf-8",
            ) as handle:
                content = yaml.safe_load(handle)
        except OSError as exc:
            raise ConfigurationError(str(exc)) from exc
        except yaml.YAMLError as exc:
            raise ConfigurationError(
                f"Invalid YAML: {self.configuration_file}"
            ) from exc

        if content is None:
            return {}

        if not isinstance(content, dict):
            raise ConfigurationError("Root configuration must be a mapping.")

        return content

    @staticmethod
    def _build_paths(
        overrides: dict[str, Any],
    ) -> ProjectPaths:
        project_root = Path(overrides.get("project_root", PROJECT_ROOT))

        return ProjectPaths(
            project_root=project_root,
            datasets=project_root / DATASET_DIRECTORY,
            logs=project_root / LOG_DIRECTORY,
            reports=project_root / REPORT_DIRECTORY,
            results=project_root / RESULT_DIRECTORY,
            figures=project_root / FIGURE_DIRECTORY,
            tables=project_root / TABLE_DIRECTORY,
            workflow=project_root / WORKFLOW_DIRECTORY,
        )


def load_configuration(
    config_directory: Path | str = CONFIG_ROOT,
) -> GOHIFConfiguration:
    """
    Convenience function for loading GOHIF configuration.
    """
    return ConfigurationLoader(config_directory).load()
