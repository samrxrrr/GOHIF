"""
Base exception hierarchy.
"""

from __future__ import annotations


class GOHIFError(Exception):
    """Base exception for GOHIF."""


class ConfigurationError(GOHIFError):
    """Configuration failure."""


class StorageError(GOHIFError):
    """Storage backend failure."""


class AcquisitionError(GOHIFError):
    """Dataset acquisition failure."""


class ValidationError(GOHIFError):
    """Validation failure."""


class ProvenanceError(GOHIFError):
    """Provenance failure."""
