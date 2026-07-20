"""
GOHIF Universal Metadata Validator
Phase 3.2
"""

from pathlib import Path
import pandas as pd


SCHEMA = pd.read_csv(
    "metadata/schema/CANONICAL_METADATA_SCHEMA.csv"
)


REQUIRED_FIELDS = set(
    SCHEMA.loc[
        SCHEMA["Required"] == "YES",
        "Field_Name"
    ]
)


def validate_metadata(metadata):

    errors = []

    missing = REQUIRED_FIELDS - set(metadata.keys())

    if missing:

        errors.append(
            "Missing fields: " +
            ", ".join(sorted(missing))
        )

    return {

        "valid": len(errors) == 0,

        "errors": errors

    }


def validate_catalog(csv_file):

    df = pd.read_csv(csv_file)

    required = list(REQUIRED_FIELDS)

    missing = [
        c for c in required
        if c not in df.columns
    ]

    if missing:

        print()

        print("Missing Columns")

        for c in missing:
            print(" -", c)

        return False

    print()

    print("Catalog validation PASSED")

    print()

    print("Rows :", len(df))

    print("Columns :", len(df.columns))

    return True


if __name__ == "__main__":

    validate_catalog(
        "metadata/schema/GOHIF_MASTER_OBJECT_CATALOG.csv"
    )
