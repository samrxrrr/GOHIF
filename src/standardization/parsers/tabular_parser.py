"""
GOHIF Tabular Parser
Scientific Metadata Enrichment
Modular Refactor Version 3.0

Supports:
- TSV
- CSV
"""

from pathlib import Path

import pandas as pd

from src.standardization.base_parser import BaseParser

from src.standardization.common.metadata_builder import (
    build_metadata,
)

from src.standardization.common.validators import (
    validate_file_exists,
    validate_nonempty_file,
)


class TabularParser(BaseParser):

    PARSER_NAME = "TabularParser"
    PARSER_VERSION = "3.0"

    SUPPORTED_EXTENSIONS = {
        ".tsv",
        ".csv",
    }

    def detect(self, path):

        return (
            Path(path).suffix.lower()
            in self.SUPPORTED_EXTENSIONS
        )

    def _separator(self, path):

        path = Path(path)

        if path.suffix.lower() == ".tsv":

            return "\t"

        return ","

    def _read_table(self, path):

        path = Path(path)

        return pd.read_csv(
            path,
            sep=self._separator(path),
            low_memory=False,
        )

    def _analyze_table(self, path):

        path = Path(path)

        metadata = {

            "Rows":
                0,

            "Columns":
                0,

            "Column_Names":
                [],

            "Delimiter":
                None,

            "Missing_Values":
                0,

            "Duplicate_Rows":
                0,

            "Numeric_Columns":
                0,

            "Text_Columns":
                0,

            "Validation_Status":
                "VALID",

        }

        if not validate_file_exists(path):

            metadata[
                "Validation_Status"
            ] = "FILE_NOT_FOUND"

            return metadata

        if not validate_nonempty_file(path):

            metadata[
                "Validation_Status"
            ] = "EMPTY_FILE"

            return metadata

        separator = self._separator(path)

        metadata[
            "Delimiter"
        ] = (
            "TAB"
            if separator == "\t"
            else "COMMA"
        )

        try:

            df = self._read_table(path)

        except pd.errors.EmptyDataError:

            metadata[
                "Validation_Status"
            ] = "EMPTY_TABLE"

            return metadata

        except pd.errors.ParserError:

            metadata[
                "Validation_Status"
            ] = "PARSE_ERROR"

            return metadata

        except UnicodeDecodeError:

            metadata[
                "Validation_Status"
            ] = "ENCODING_ERROR"

            return metadata

        except OSError:

            metadata[
                "Validation_Status"
            ] = "ERROR"

            return metadata

        except Exception:

            metadata[
                "Validation_Status"
            ] = "ERROR"

            return metadata

        metadata[
            "Rows"
        ] = len(df)

        metadata[
            "Columns"
        ] = len(df.columns)

        metadata[
            "Column_Names"
        ] = list(df.columns)

        metadata[
            "Missing_Values"
        ] = int(
            df.isna()
            .sum()
            .sum()
        )

        metadata[
            "Duplicate_Rows"
        ] = int(
            df.duplicated()
            .sum()
        )

        numeric_columns = (
            df.select_dtypes(
                include="number"
            )
            .columns
        )

        metadata[
            "Numeric_Columns"
        ] = len(
            numeric_columns
        )

        metadata[
            "Text_Columns"
        ] = (
            len(df.columns)
            - len(numeric_columns)
        )

        return metadata

    def extract_metadata(self, path):

        path = Path(path)

        analysis = self._analyze_table(
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

        analysis = self._analyze_table(
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

        path = Path(path)

        df = self._read_table(path)

        output_dir = Path(
            output_dir
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        out = (
            output_dir
            / (
                path.stem
                + ".csv"
            )
        )

        df.to_csv(
            out,
            index=False,
        )

        return out

    def summarize(self, path):

        return self.extract_metadata(
            path
        )
