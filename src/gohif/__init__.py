"""
Global One Health Intelligence Framework (GOHIF)
================================================

GOHIF is a reusable scientific framework for developing reproducible,
modular, and production-quality One Health computational workflows.

This package exposes framework-level metadata.
"""

from .config.constants import FRAMEWORK_VERSION
from .config.constants import PROJECT_NAME
from .config.constants import PROJECT_SHORT_NAME

__all__ = [
    "FRAMEWORK_VERSION",
    "PROJECT_NAME",
    "PROJECT_SHORT_NAME",
]

__version__ = FRAMEWORK_VERSION
__title__ = PROJECT_NAME
__package_name__ = PROJECT_SHORT_NAME
