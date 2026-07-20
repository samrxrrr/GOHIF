"""
GOHIF JSON Parser
Phase 3 Standardization

Handles:
- Valid JSON
- Empty JSON files
- Invalid JSON files

Author: GOHIF
"""

from pathlib import Path
import json

from src.standardization.base_parser import BaseParser


class JSONParser(BaseParser):

    def detect(self, path):
        return Path(path).suffix.lower() == ".json"

    def extract_metadata(self, path):

        path = Path(path)

        size_mb = round(path.stat().st_size / 1024 / 1024, 6)

        metadata = {
            "Filename": path.name,
            "File_Size_MB": size_mb,
            "SHA256": self.sha256(path),
            "JSON_Type": None,
            "Top_Level_Items": 0,
            "Validation_Status": "VALID"
        }

        # Empty file
        if path.stat().st_size == 0:
            metadata["Validation_Status"] = "EMPTY_FILE"
            return metadata

        try:

            with open(path, "r", encoding="utf-8") as f:
                obj = json.load(f)

            metadata["JSON_Type"] = type(obj).__name__

            if hasattr(obj, "__len__"):
                metadata["Top_Level_Items"] = len(obj)
            else:
                metadata["Top_Level_Items"] = 1

            return metadata

        except json.JSONDecodeError:

            metadata["Validation_Status"] = "INVALID_JSON"
            return metadata

        except Exception:

            metadata["Validation_Status"] = "ERROR"
            return metadata


    def validate(self, path):

        meta = self.extract_metadata(path)

        return meta["Validation_Status"] == "VALID"


    def standardize(self, path, output_dir):

        return path


    def summarize(self, path):

        return self.extract_metadata(path)
