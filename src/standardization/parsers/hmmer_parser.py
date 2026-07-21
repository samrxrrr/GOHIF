"""
GOHIF HMMER Database Parser
Modular Refactor Version 3.0

Supports HMMER pressed profile database components:
- .h3f
- .h3i
- .h3m
- .h3p
"""

from pathlib import Path

from src.standardization.base_parser import BaseParser

from src.standardization.common.metadata_builder import (
    build_metadata,
)

from src.standardization.common.validators import (
    validate_file_exists,
    validate_nonempty_file,
    validate_binary_readable,
)


class HMMERParser(BaseParser):

    PARSER_NAME = "HMMERParser"
    PARSER_VERSION = "3.0"

    SUPPORTED_EXTENSIONS = {
        ".h3f",
        ".h3i",
        ".h3m",
        ".h3p",
    }

    COMPONENT_TYPES = {
        ".h3f": "FILTER_DATA",
        ".h3i": "SSI_INDEX",
        ".h3m": "PROFILE_MODELS",
        ".h3p": "PRESSED_PROFILES",
    }

    def detect(self, path):

        return (
            Path(path).suffix.lower()
            in self.SUPPORTED_EXTENSIONS
        )

    def _database_prefix(self, path):

        path = Path(path)

        return path.with_suffix("").name

    def _component_inventory(self, path):

        path = Path(path)

        prefix = path.with_suffix("")

        components = {}

        for extension in sorted(
            self.SUPPORTED_EXTENSIONS
        ):

            component = Path(
                str(prefix) + extension
            )

            components[extension] = (
                component.exists()
                and component.is_file()
            )

        return components

    def _analyze(self, path):

        path = Path(path)

        extension = path.suffix.lower()

        components = (
            self._component_inventory(path)
        )

        component_count = sum(
            components.values()
        )

        complete_database = (
            component_count
            == len(
                self.SUPPORTED_EXTENSIONS
            )
        )

        if not validate_file_exists(path):

            status = "FILE_NOT_FOUND"

        elif not validate_nonempty_file(path):

            status = "EMPTY_FILE"

        elif not validate_binary_readable(path):

            status = "READ_ERROR"

        else:

            status = "VALID"

        return {

            "Database_Name":
                self._database_prefix(path),

            "HMMER_Component":
                self.COMPONENT_TYPES.get(
                    extension,
                    "UNKNOWN",
                ),

            "Component_Extension":
                extension,

            "Component_Count":
                component_count,

            "Expected_Component_Count":
                len(
                    self.SUPPORTED_EXTENSIONS
                ),

            "Complete_HMMER_Database":
                complete_database,

            "H3F_Present":
                components.get(
                    ".h3f",
                    False,
                ),

            "H3I_Present":
                components.get(
                    ".h3i",
                    False,
                ),

            "H3M_Present":
                components.get(
                    ".h3m",
                    False,
                ),

            "H3P_Present":
                components.get(
                    ".h3p",
                    False,
                ),

            "Validation_Status":
                status,
        }

    def extract_metadata(self, path):

        path = Path(path)

        analysis = self._analyze(
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

        analysis = self._analyze(
            path
        )

        return (
            analysis[
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
