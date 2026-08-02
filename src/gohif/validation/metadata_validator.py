from pathlib import Path
import json

REQUIRED_FIELDS = [
    "dataset_id",
    "dataset_name",
    "domain",
    "dataset_type",
    "dataset_path",
    "files",
]


class MetadataValidator:

    def validate(self, metadata_file):

        metadata_file = Path(metadata_file)

        errors = []

        try:

            with open(metadata_file, encoding="utf-8") as f:
                data = json.load(f)

        except Exception as e:

            return False, [str(e)]

        for field in REQUIRED_FIELDS:

            if field not in data:

                errors.append(
                    f"Missing field: {field}"
                )

        if not isinstance(data.get("files", []), list):

            errors.append(
                "'files' must be a list"
            )

        return len(errors) == 0, errors


if __name__ == "__main__":

    validator = MetadataValidator()

    metadata_dir = Path("/mnt/g/My Drive/DATASETS/_metadata")

    total = 0
    passed = 0
    failed = 0

    print("=" * 70)
    print("GOHIF Metadata Validation")
    print("=" * 70)

    for file in sorted(metadata_dir.glob("GOHIF_DS_*.json")):

        ok, errors = validator.validate(file)

        total += 1

        if ok:

            passed += 1

            print(f"[PASS] {file.name}")

        else:

            failed += 1

            print(f"[FAIL] {file.name}")

            for e in errors:

                print("   ", e)

    print("=" * 70)
    print(f"Total : {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("=" * 70)
