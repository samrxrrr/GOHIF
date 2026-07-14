"""
GOHIF Configuration Package
===========================

Configuration subsystem for the Global One Health Intelligence
Framework (GOHIF).

This package provides:

- Configuration constants
- Configuration exceptions
- Configuration models
"""

from .config_models import GOHIFConfiguration
from .config_models import ProjectPaths
from .config_models import RuntimeConfiguration
from .constants import FRAMEWORK_VERSION
from .constants import PROJECT_NAME
from .constants import PROJECT_SHORT_NAME
from .exceptions import ConfigurationError

__all__ = [
    "GOHIFConfiguration",
    "ProjectPaths",
    "RuntimeConfiguration",
    "ConfigurationError",
    "FRAMEWORK_VERSION",
    "PROJECT_NAME",
    "PROJECT_SHORT_NAME",
]
