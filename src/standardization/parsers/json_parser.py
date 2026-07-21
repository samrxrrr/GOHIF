"""
GOHIF JSON Parser
Scientific Metadata Enrichment
Modular Refactor Version 3.0

Handles:
- Valid JSON
- Empty JSON files
- Invalid JSON files
- Read/decoding errors
"""

import json
from pathlib import Path

from src.standardization.base_parser import BaseParser

from src.standardization.common.metadata_builder import (
    build_metadata,
)

from src.standardization.common.validators import (
    validate_file_exists,
)


class JSONParser(BaseParser):

    PARSER_NAME = "JSONParser"
    PARSER_VERSION = "3.0"

    SUPPORTED_EXTENSIONS = {
        ".json",
    }

    def detect(self, path):

        return (
            Path(path).suffix.lower()
            in self.SUPPORTED_EXTENSIONS
        )

    def _analyze_json(self, path):

        path = Path(path)

        result = {

            "JSON_Type":
                None,

            "Top_Level_Items":
                0,

            "Top_Level_Keys":
                None,

            "Validation_Status":
                "VALID",

        }

        if not validate_file_exists(path):

            result[
                "Validation_Status"
            ] = "FILE_NOT_FOUND"

            return result

        if path.stat().st_size == 0:

            result[
                "Validation_Status"
            ] = "EMPTY_FILE"

            return result

        try:

            with path.open(
                "r",
                encoding="utf-8",
            ) as handle:

                obj = json.load(handle)

        except json.JSONDecodeError:

            result[
                "Validation_Status"
            ] = "INVALID_JSON"

            return result

        except UnicodeDecodeError:

            result[
                "Validation_Status"
            ] = "ENCODING_ERROR"

            return result

        except OSError:

            result[
                "Validation_Status"
            ] = "ERROR"

            return result

        except Exception:

            result[
                "Validation_Status"
            ] = "ERROR"

            return result

        result[
            "JSON_Type"
        ] = type(obj).__name__

        if hasattr(
            obj,
            "__len__",
        ):

            try:

                result[
                    "Top_Level_Items"
                ] = len(obj)

            except TypeError:

                result[
                    "Top_Level_Items"
                ] = 1

        else:

            result[
                "Top_Level_Items"
            ] = 1

        if isinstance(
            obj,
            dict,
        ):

            result[
                "Top_Level_Keys"
            ] = list(
                obj.keys()
            )

        return result

    def extract_metadata(self, path):

        path = Path(path)

        analysis = self._analyze_json(
            path
        )

        status = analysis.pop(
            "Validation_Status"
        )

        return build_metadata(
            path=path,
            parser_name=self.PARSER_NAME,
            parser_version=self.PARSER_VERSION,
            scientific_metadata=analysis,
            validation_status=status,
        )

    def validate(self, path):

        result = self._analyze_json(
            path
        )

        return (
            result[
                "Validation_Status"
            ]
            == "VALID"
        )

    def standardize(
        self,
        path,
        output_dir,
    ):

        return path

    def summarize(self, path):

        return self.extract_metadata(
            path
        )
