import hashlib
import json
from pathlib import Path


class ArtifactValidator:

    @staticmethod
    def validate(metadata_file):

        metadata_file = Path(metadata_file)

        meta = json.load(
            open(metadata_file)
        )

        csv = metadata_file.with_suffix("").with_suffix(".csv")

        sha = hashlib.sha256(
            csv.read_bytes()
        ).hexdigest()

        if sha != meta["sha256"]:

            print("FAILED")

            return False

        print("PASSED")

        return True
