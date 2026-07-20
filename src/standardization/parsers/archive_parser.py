"""
GOHIF Archive Parser

Supports ZIP, TAR, GZIP and related archive formats.
"""

from pathlib import Path
import zipfile
import tarfile
import gzip

from src.standardization.base_parser import BaseParser


class ArchiveParser(BaseParser):

    def detect(self, path):
        return True

    def extract_metadata(self, path):

        path = Path(path)

        members = None

        try:

            if zipfile.is_zipfile(path):
                with zipfile.ZipFile(path) as z:
                    members = len(z.namelist())

            elif tarfile.is_tarfile(path):
                with tarfile.open(path) as t:
                    members = len(t.getmembers())

            elif path.suffix.lower() == ".gz":
                members = 1

        except Exception:
            members = None

        return {

            "Filename": path.name,

            "Extension": path.suffix.lower(),

            "File_Size_MB":
                round(path.stat().st_size / 1024 / 1024, 6),

            "Archive_Members": members,

            "SHA256":
                self.sha256(path),

            "Validation_Status":
                "VALID",

            "Parser_Name":
                "ArchiveParser",

            "Parser_Version":
                "1.0"

        }

    def validate(self, path):
        return True

    def standardize(self, path, output_dir):
        return path

    def summarize(self, path):
        return self.extract_metadata(path)
