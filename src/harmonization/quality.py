"""
GOHIF Metadata Quality Engine

Phase 7.5
"""

from pathlib import Path

import pandas as pd

from src.harmonization.schema import SCHEMA


ROOT = Path(__file__).resolve().parents[2]

INPUT = ROOT / "metadata/schema/GOHIF_CANONICAL_METADATA.csv"

OUTPUT_DIR = ROOT / "metadata/schema"


class MetadataQualityEngine:

    def __init__(self):

        self.required_fields = SCHEMA.fields()

    def load(self):

        return pd.read_csv(INPUT)

    def field_completeness(self, df):

        rows = []

        total = len(df)

        for field in df.columns:

            populated = int(df[field].notna().sum())

            rows.append({

                "Field": field,

                "Populated": populated,

                "Missing": total - populated,

                "Completeness_Percent":
                    round(
                        populated /
                        total *
                        100,
                        2,
                    ),

                "Canonical_Field":
                    field in self.required_fields,

            })

        return pd.DataFrame(rows)

    def dataset_quality(self, df):

        rows = []

        canonical = [

            c

            for c in self.required_fields

            if c in df.columns

        ]

        total = len(canonical)

        for _, row in df.iterrows():

            populated = int(

                row[canonical]

                .notna()

                .sum()

            )

            rows.append({

                "Dataset_Name":

                    row.get(

                        "Dataset_Name",

                        None,

                    ),

                "Parser_Name":

                    row.get(

                        "Parser_Name",

                        None,

                    ),

                "Validation_Status":

                    row.get(

                        "Validation_Status",

                        None,

                    ),

                "Canonical_Fields":

                    total,

                "Populated":

                    populated,

                "Completeness_Percent":

                    round(

                        populated /

                        total *

                        100,

                        2,

                    ),

            })

        return pd.DataFrame(rows)

    def schema_compliance(self, df):

        rows = []

        for field in self.required_fields:

            rows.append({

                "Canonical_Field":

                    field,

                "Present":

                    field in df.columns,

            })

        return pd.DataFrame(rows)

    def run(self):

        df = self.load()

        field_df = self.field_completeness(df)

        dataset_df = self.dataset_quality(df)

        schema_df = self.schema_compliance(df)

        field_df.to_csv(

            OUTPUT_DIR /

            "GOHIF_FIELD_COMPLETENESS.csv",

            index=False,

        )

        dataset_df.to_csv(

            OUTPUT_DIR /

            "GOHIF_METADATA_QUALITY_REPORT.csv",

            index=False,

        )

        schema_df.to_csv(

            OUTPUT_DIR /

            "GOHIF_SCHEMA_COMPLIANCE.csv",

            index=False,

        )

        print()

        print("=" * 72)

        print("GOHIF METADATA QUALITY ENGINE")

        print("=" * 72)

        print()

        print(

            "Datasets:",

            len(df),

        )

        print(

            "Canonical Fields:",

            len(self.required_fields),

        )

        print(

            "Total Columns:",

            len(df.columns),

        )

        print()

        print(

            "Reports generated"

        )

        print()

        print(

            OUTPUT_DIR /

            "GOHIF_FIELD_COMPLETENESS.csv"

        )

        print(

            OUTPUT_DIR /

            "GOHIF_METADATA_QUALITY_REPORT.csv"

        )

        print(

            OUTPUT_DIR /

            "GOHIF_SCHEMA_COMPLIANCE.csv"

        )


ENGINE = MetadataQualityEngine()


if __name__ == "__main__":

    ENGINE.run()
