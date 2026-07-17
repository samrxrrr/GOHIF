"""
GOHIF exception hierarchy.
"""

from .base import (
    AcquisitionError,
    ConfigurationError,
    GOHIFError,
    ProvenanceError,
    StorageError,
    ValidationError,
)

__all__ = [
    "GOHIFError",
    "ConfigurationError",
    "StorageError",
    "AcquisitionError",
    "ValidationError",
    "ProvenanceError",
]
