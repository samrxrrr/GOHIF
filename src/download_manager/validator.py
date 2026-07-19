"""
GOHIF Download Validator
Author: GOHIF
"""

from pathlib import Path
import json
import zipfile
import hashlib


class Validator:
    """
    Validation utilities for downloaded datasets.
    """

    @staticmethod
    def exists(path):
        return Path(path).exists()

    @staticmethod
    def non_empty(path):
        p = Path(path)
        return p.exists() and p.stat().st_size > 0

    @staticmethod
    def file_size_mb(path):
        return round(Path(path).stat().st_size / (1024 * 1024), 3)

    @staticmethod
    def sha256(path):

        h = hashlib.sha256()

        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)

        return h.hexdigest()

    @staticmethod
    def is_zip(path):

        try:
            return zipfile.is_zipfile(path)
        except Exception:
            return False

    @staticmethod
    def is_json(path):

        try:

            with open(path, encoding="utf-8") as f:
                json.load(f)

            return True

        except Exception:
            return False

    @staticmethod
    def is_fasta(path):

        try:

            with open(path) as f:

                first = f.readline()

            return first.startswith(">")

        except Exception:
            return False

    @staticmethod
    def is_fastq(path):

        try:

            with open(path) as f:

                first = f.readline()

            return first.startswith("@")

        except Exception:
            return False

    @staticmethod
    def is_html(path):

        try:

            with open(path, encoding="utf-8", errors="ignore") as f:

                first = f.readline().lower()

            return (
                "<html" in first
                or "<!doctype html" in first
            )

        except Exception:
            return False

    @staticmethod
    def validate(path, expected):

        if not Validator.exists(path):
            return False

        if not Validator.non_empty(path):
            return False

        expected = expected.upper()

        if expected == "ZIP":
            return Validator.is_zip(path)

        if expected == "JSON":
            return Validator.is_json(path)

        if expected == "FASTA":
            return Validator.is_fasta(path)

        if expected == "FASTQ":
            return Validator.is_fastq(path)

        return True


if __name__ == "__main__":

    print("Validator Ready")
