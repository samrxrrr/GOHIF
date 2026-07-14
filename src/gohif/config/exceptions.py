"""
GOHIF Configuration Exceptions
==============================

Project:
    Global One Health Intelligence Framework (GOHIF)

Module:
    gohif.config.exceptions

Purpose:
    Defines the exception hierarchy used by the GOHIF
    configuration subsystem.

Author:
    GOHIF Development Team

Version:
    0.2.0
"""

from pathlib import Path


class ConfigurationError(Exception):
    """
    Base exception for all configuration-related errors.
    """

    def __init__(self, message: str):
        super().__init__(message)


class MissingConfigurationError(ConfigurationError):
    """
    Raised when a required configuration file cannot be found.
    """

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        super().__init__(f"Required configuration file not found: {self.file_path}")


class InvalidConfigurationError(ConfigurationError):
    """
    Raised when a configuration file exists but contains
    invalid or malformed content.
    """

    def __init__(
        self,
        file_path: str | Path,
        reason: str,
    ):
        self.file_path = Path(file_path)
        self.reason = reason

        super().__init__(f"Invalid configuration in '{self.file_path}': {reason}")


class ConfigurationValidationError(ConfigurationError):
    """
    Raised when configuration validation fails.
    """

    def __init__(
        self,
        file_path: str | Path,
        validation_errors: list[str],
    ):
        self.file_path = Path(file_path)
        self.validation_errors = validation_errors

        formatted_errors = "\n".join(f"  - {error}" for error in validation_errors)

        message = (
            f"Configuration validation failed for "
            f"'{self.file_path}'.\n"
            f"Errors:\n{formatted_errors}"
        )

        super().__init__(message)


class UnsupportedConfigurationFormatError(ConfigurationError):
    """
    Raised when an unsupported configuration file extension
    is encountered.
    """

    def __init__(
        self,
        file_path: str | Path,
        supported_extensions: tuple[str, ...],
    ):
        self.file_path = Path(file_path)
        self.supported_extensions = supported_extensions

        supported = ", ".join(supported_extensions)

        super().__init__(
            f"Unsupported configuration format "
            f"'{self.file_path}'. "
            f"Supported formats: {supported}"
        )


class DuplicateConfigurationKeyError(ConfigurationError):
    """
    Raised when duplicate keys are detected in a configuration file.
    """

    def __init__(
        self,
        key: str,
        file_path: str | Path,
    ):
        self.key = key
        self.file_path = Path(file_path)

        super().__init__(
            f"Duplicate configuration key '{key}' " f"found in '{self.file_path}'."
        )


class MissingRequiredKeyError(ConfigurationError):
    """
    Raised when a required configuration key is missing.
    """

    def __init__(
        self,
        key: str,
        file_path: str | Path,
    ):
        self.key = key
        self.file_path = Path(file_path)

        super().__init__(
            f"Missing required configuration key " f"'{key}' in '{self.file_path}'."
        )


class InvalidConfigurationTypeError(ConfigurationError):
    """
    Raised when a configuration value has an unexpected type.
    """

    def __init__(
        self,
        key: str,
        expected_type: str,
        actual_type: str,
    ):
        self.key = key
        self.expected_type = expected_type
        self.actual_type = actual_type

        super().__init__(
            f"Configuration key '{key}' has invalid type. "
            f"Expected '{expected_type}', "
            f"received '{actual_type}'."
        )
