"""
GOHIF Field Mapper

Phase 7.3

Maps parser-specific metadata into the
canonical GOHIF metadata schema.
"""

from copy import deepcopy

from src.harmonization.schema import SCHEMA


class FieldMapper:

    def __init__(self):

        self.mapping = deepcopy(
            SCHEMA.field_mapping
        )

    def canonical_name(self, field):

        return self.mapping.get(
            field,
            field,
        )

    def map_metadata(self, metadata):

        canonical = {}

        for key, value in metadata.items():

            canonical[
                self.canonical_name(key)
            ] = value

        return canonical

    def mapped_fields(self, metadata):

        return sorted(

            key

            for key in metadata

            if key in self.mapping

        )

    def unmapped_fields(self, metadata):

        return sorted(

            key

            for key in metadata

            if key not in self.mapping

        )

    def statistics(self, metadata):

        mapped = self.mapped_fields(
            metadata
        )

        unmapped = self.unmapped_fields(
            metadata
        )

        total = len(metadata)

        coverage = 0.0

        if total > 0:

            coverage = round(
                len(mapped) / total * 100,
                2,
            )

        return {

            "Input_Fields": total,

            "Mapped": len(mapped),

            "Unmapped": len(unmapped),

            "Coverage_Percent": coverage,

        }


FIELD_MAPPER = FieldMapper()


if __name__ == "__main__":

    sample = {

        "Filename": "example.fasta",

        "Rows": 125,

        "Columns": 5,

        "SHA256": "abcdef",

        "Parser_Name": "FASTAParser",

        "Parser_Version": "3.0",

        "Validation_Status": "VALID",

        "Unknown_Field": "demo",

    }

    canonical = FIELD_MAPPER.map_metadata(sample)

    print()

    print("=" * 72)
    print("ORIGINAL")
    print("=" * 72)

    for k, v in sample.items():
        print(f"{k:25} {v}")

    print()

    print("=" * 72)
    print("CANONICAL")
    print("=" * 72)

    for k, v in canonical.items():
        print(f"{k:25} {v}")

    print()

    print("=" * 72)
    print("STATISTICS")
    print("=" * 72)

    stats = FIELD_MAPPER.statistics(sample)

    for k, v in stats.items():
        print(f"{k:20} {v}")
