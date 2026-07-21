"""
GOHIF Metadata Builder

Centralized utilities for constructing consistent parser metadata records.
"""

from datetime import datetime, timezone
from pathlib import Path

from src.standardization.common.checksum import sha256
from src.standardization.common.file_metadata import basic_file_metadata


def utc_timestamp():
    """
    Return current UTC timestamp in ISO 8601 format.
    """

    return datetime.now(
        timezone.utc
    ).isoformat()


def clean_metadata(metadata):
    """
    Normalize metadata values for safe downstream serialization.

    Path objects are converted to strings.
    Other values are preserved.
    """

    cleaned = {}

    for key, value in metadata.items():

        if isinstance(value, Path):
            value = str(value)

        cleaned[key] = value

    return cleaned


def build_base_metadata(
    path,
    parser_name,
    parser_version,
    validation_status="VALID",
    include_checksum=True,
):
    """
    Construct canonical metadata shared by GOHIF parsers.
    """

    path = Path(path)

    metadata = basic_file_metadata(path)

    if include_checksum:

        metadata["SHA256"] = sha256(path)

    metadata.update({

        "Validation_Status":
            validation_status,

        "Parser_Name":
            parser_name,

        "Parser_Version":
            parser_version,

        "Created_UTC":
            utc_timestamp(),

    })

    return clean_metadata(metadata)


def merge_metadata(
    base_metadata,
    scientific_metadata=None,
    overwrite=True,
):
    """
    Merge base metadata with parser-specific scientific metadata.

    Parameters
    ----------
    base_metadata : dict
        Canonical base metadata.

    scientific_metadata : dict or None
        Format-specific metadata.

    overwrite : bool
        If True, scientific metadata may replace existing keys.

    Returns
    -------
    dict
    """

    result = dict(base_metadata)

    if not scientific_metadata:

        return clean_metadata(result)

    for key, value in scientific_metadata.items():

        if overwrite or key not in result:

            result[key] = value

    return clean_metadata(result)


def build_metadata(
    path,
    parser_name,
    parser_version,
    scientific_metadata=None,
    validation_status="VALID",
    include_checksum=True,
):
    """
    Build a complete GOHIF parser metadata record.
    """

    base = build_base_metadata(
        path=path,
        parser_name=parser_name,
        parser_version=parser_version,
        validation_status=validation_status,
        include_checksum=include_checksum,
    )

    return merge_metadata(
        base_metadata=base,
        scientific_metadata=scientific_metadata,
        overwrite=True,
    )
