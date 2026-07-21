"""
GOHIF Common Validation Utilities

Shared validation functions for the standardization and parser framework.
"""

from pathlib import Path


def validate_file_exists(path):
    """Return True when path exists and is a regular file."""

    path = Path(path)

    return path.exists() and path.is_file()


def validate_nonempty_file(path):
    """Return True when path is an existing non-empty regular file."""

    path = Path(path)

    return (
        path.exists()
        and path.is_file()
        and path.stat().st_size > 0
    )


def validate_extension(path, allowed_extensions):
    """
    Validate a file extension against an allowed collection.

    Extensions may be supplied with or without a leading dot.
    Matching is case-insensitive.
    """

    path = Path(path)

    normalized = {
        ext.lower()
        if str(ext).startswith(".")
        else f".{str(ext).lower()}"
        for ext in allowed_extensions
    }

    return path.suffix.lower() in normalized


def validate_text_readable(path, encoding="utf-8"):
    """
    Check whether a file can be read as text.

    Invalid byte sequences are replaced so that biological/database text
    files with occasional encoding anomalies remain inspectable.
    """

    path = Path(path)

    if not validate_file_exists(path):
        return False

    try:

        with path.open(
            "r",
            encoding=encoding,
            errors="replace"
        ) as handle:

            handle.read(4096)

        return True

    except (OSError, UnicodeError):

        return False


def validate_binary_readable(path):
    """Check whether a file can be opened and sampled in binary mode."""

    path = Path(path)

    if not validate_file_exists(path):
        return False

    try:

        with path.open("rb") as handle:

            handle.read(4096)

        return True

    except OSError:

        return False


def validate_fasta_structure(path):
    """
    Perform lightweight FASTA structural validation.

    A valid candidate must be non-empty and contain at least one
    header beginning with '>'.
    """

    path = Path(path)

    if not validate_nonempty_file(path):
        return False

    try:

        with path.open(
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as handle:

            for line in handle:

                line = line.strip()

                if not line:
                    continue

                return line.startswith(">")

    except OSError:

        return False

    return False


def validate_fastq_structure(path):
    """
    Perform lightweight FASTQ structural validation.

    Validates the first complete FASTQ record:
    header, sequence, plus-line and quality string.
    """

    path = Path(path)

    if not validate_nonempty_file(path):
        return False

    try:

        with path.open(
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as handle:

            header = handle.readline().rstrip("\r\n")
            sequence = handle.readline().rstrip("\r\n")
            plus = handle.readline().rstrip("\r\n")
            quality = handle.readline().rstrip("\r\n")

        if not header.startswith("@"):
            return False

        if not plus.startswith("+"):
            return False

        if not sequence:
            return False

        if len(sequence) != len(quality):
            return False

        return True

    except OSError:

        return False


def validation_status(is_valid):
    """Convert a Boolean validation result to canonical GOHIF status."""

    return "VALID" if bool(is_valid) else "INVALID"
