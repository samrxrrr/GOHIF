"""
GOHIF HMMER Database Parser

Supports HMMER profile database files.
"""

from pathlib import Path

from src.standardization.base_parser import BaseParser


class HMMERParser(BaseParser):

    def detect(self, path):
        return True

    def extract_metadata(self, path):

        path = Path(path)

        return {

            "Filename": path.name,

            "Extension": path.suffix.lower(),

            "File_Size_MB":
                round(path.stat().st_size / 1024 / 1024, 6),

            "SHA256":
                self.sha256(path),

            "Validation_Status":
                "VALID",

            "Parser_Name":
                "HMMERParser",

            "Parser_Version":
                "1.0"

        }

    def validate(self, path):
        return True

    def standardize(self, path, output_dir):
        return path

    def summarize(self, path):
        return self.extract_metadata(path)
