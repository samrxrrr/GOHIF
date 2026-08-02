from pathlib import Path
import json

from gohif.standardization.schema import GOHIF_SCHEMA


class SchemaMapper:

    def __init__(self):

        self.input_dir = Path("/mnt/g/My Drive/DATASETS/_metadata")

        self.output_dir = Path("/mnt/g/My Drive/DATASETS/_metadata_standardized")

        self.output_dir.mkdir(exist_ok=True)

    def empty_schema(self):

        obj = {}

        for key, dtype in GOHIF_SCHEMA.items():

            if dtype is list:
                obj[key] = []

            elif dtype is bool:
                obj[key] = False

            elif dtype is int:
                obj[key] = 0

            else:
                obj[key] = ""

        return obj

    def map_metadata(self, metadata_file):

        with open(metadata_file, encoding="utf-8") as f:

            source = json.load(f)

        target = self.empty_schema()

        target["dataset_id"] = source.get("dataset_id", "")
        target["dataset_name"] = source.get("dataset_name", "")
        target["title"] = source.get("dataset_name", "")
        target["domain"] = source.get("domain", "")
        target["dataset_type"] = source.get("dataset_type", "")
        target["dataset_path"] = source.get("dataset_path", "")
        target["file_count"] = len(source.get("files", []))
        target["metadata_version"] = "1.0"
        target["standardized"] = True

        outfile = self.output_dir / metadata_file.name

        with open(outfile, "w", encoding="utf-8") as f:

            json.dump(target, f, indent=2)

        return outfile

    def run(self):

        total = 0

        for file in sorted(self.input_dir.glob("GOHIF_DS_*.json")):

            self.map_metadata(file)

            total += 1

        print("=" * 70)
        print("GOHIF Schema Mapper")
        print("=" * 70)
        print("Datasets standardized :", total)
        print("Output directory      :", self.output_dir)
        print("=" * 70)


if __name__ == "__main__":

    SchemaMapper().run()
