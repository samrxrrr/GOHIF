"""
GOHIF Canonical Metadata Schema

Phase 7.2
"""

from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[2]

SCHEMA_DIR = ROOT / "metadata" / "schema"


class CanonicalSchema:

    def __init__(self):

        self.schema = self._load_yaml(
            "canonical_schema.yaml"
        )

        self.vocabularies = self._load_yaml(
            "controlled_vocabularies.yaml"
        )

        self.field_mapping = self._load_yaml(
            "field_mapping.yaml"
        )

    def _load_yaml(self, filename):

        path = SCHEMA_DIR / filename

        with open(path, "r", encoding="utf-8") as f:

            return yaml.safe_load(f)

    @property
    def version(self):

        return str(
            self.schema.get(
                "version",
                "unknown",
            )
        )

    def sections(self):

        return [
            k
            for k in self.schema.keys()
            if k != "version"
        ]

    def fields(self):

        result = []

        for section in self.sections():

            result.extend(
                self.schema[section]
            )

        return result

    def vocabulary(self, name):

        return self.vocabularies.get(
            name,
            [],
        )

    def map_field(self, field):

        return self.field_mapping.get(
            field,
            field,
        )

    def has_field(self, field):

        return field in self.fields()

    def summary(self):

        print()

        print("=" * 72)
        print("GOHIF CANONICAL METADATA SCHEMA")
        print("=" * 72)

        print("Version:", self.version)

        print()

        for section in self.sections():

            print(
                f"{section:15}",
                len(
                    self.schema[section]
                ),
                "fields",
            )

        print()

        print(
            "Total Fields:",
            len(
                self.fields()
            )
        )

        print(
            "Controlled Vocabularies:",
            len(
                self.vocabularies
            )
        )

        print(
            "Field Mappings:",
            len(
                self.field_mapping
            )
        )


SCHEMA = CanonicalSchema()


if __name__ == "__main__":

    SCHEMA.summary()
