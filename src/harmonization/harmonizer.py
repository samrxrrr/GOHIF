"""
GOHIF Metadata Harmonizer

Phase 7.4

Converts parser metadata into the
canonical GOHIF metadata schema.
"""

from pathlib import Path

import pandas as pd

from src.harmonization.field_mapper import FIELD_MAPPER
from src.harmonization.schema import SCHEMA


class MetadataHarmonizer:

    def __init__(self):

        self.required_fields = SCHEMA.fields()

    def harmonize_record(self, record):

        record = dict(record)

        canonical = FIELD_MAPPER.map_metadata(record)

        output = {}

        for field in self.required_fields:

            output[field] = canonical.get(field, None)

        for key, value in canonical.items():

            if key not in output:

                output[key] = value

        return output

    def harmonize_dataframe(self, df):

        rows = []

        for _, row in df.iterrows():

            rows.append(

                self.harmonize_record(

                    row.to_dict()

                )

            )

        return pd.DataFrame(rows)

    def harmonize_csv(self, input_csv, output_csv):

        df = pd.read_csv(input_csv)

        result = self.harmonize_dataframe(df)

        output_csv = Path(output_csv)

        output_csv.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        result.to_csv(
            output_csv,
            index=False
        )

        return result


HARMONIZER = MetadataHarmonizer()


if __name__ == "__main__":

    INPUT = "metadata/schema/MASTER_METADATA_CATALOG.csv"

    OUTPUT = "metadata/schema/GOHIF_CANONICAL_METADATA.csv"

    df = HARMONIZER.harmonize_csv(
        INPUT,
        OUTPUT
    )

    print()

    print("="*72)
    print("GOHIF METADATA HARMONIZER")
    print("="*72)

    print("Rows:",len(df))
    print("Columns:",len(df.columns))

    print()

    print("Output")

    print(OUTPUT)
