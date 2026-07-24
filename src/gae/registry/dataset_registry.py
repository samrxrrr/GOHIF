from __future__ import annotations

import csv
from pathlib import Path


class DatasetRegistry:

    def __init__(
        self,
        registry_file: Path,
    ):
        self.registry_file = registry_file

    def manifests(self):

        manifests = []

        with self.registry_file.open(
            newline=""
        ) as handle:

            reader = csv.DictReader(handle)

            rows = sorted(
                reader,
                key=lambda r: int(r["priority"])
            )

            for row in rows:

                if row["enabled"].lower() != "true":
                    continue

                manifests.append(
                    Path(row["manifest"])
                )

        return manifests
