from pathlib import Path
import hashlib
import json
import zipfile

import pandas as pd


class PostProcessor:

    def process(
        self,
        file: Path,
        checksum=None,
    ):

        file = Path(file)

        profile = {
            "file": str(file),
            "name": file.name,
            "extension": file.suffix,
            "size": file.stat().st_size,
        }

        h = hashlib.sha256()

        with open(file, "rb") as f:

            while True:

                b = f.read(1024 * 1024)

                if not b:
                    break

                h.update(b)

        profile["sha256"] = h.hexdigest()

        try:

            if file.suffix.lower() == ".csv":

                df = pd.read_csv(file, nrows=500)

                profile["type"] = "csv"
                profile["columns"] = list(df.columns)
                profile["column_count"] = len(df.columns)
                profile["sample_rows"] = len(df)

            elif file.suffix.lower() == ".json":

                obj = json.load(open(file))

                profile["type"] = "json"

                if isinstance(obj, dict):

                    profile["keys"] = list(obj.keys())

                elif isinstance(obj, list):

                    profile["records"] = len(obj)

            elif file.suffix.lower() in (
                ".fa",
                ".fasta",
                ".faa",
                ".fna",
            ):

                n = 0

                with open(file) as f:

                    for line in f:

                        if line.startswith(">"):
                            n += 1

                profile["type"] = "fasta"
                profile["sequence_count"] = n

            elif file.suffix.lower() == ".zip":

                z = zipfile.ZipFile(file)

                profile["type"] = "zip"
                profile["files"] = z.namelist()

        except Exception as e:

            profile["error"] = str(e)

        out = (
            Path.home()
            / "GoogleDrive"
            / "GOHIF_DATA"
            / "01_METADATA"
            / "Profiles"
        )

        out.mkdir(parents=True, exist_ok=True)

        outfile = out / (file.name + ".profile.json")

        json.dump(
            profile,
            open(outfile, "w"),
            indent=2,
        )

        return profile
