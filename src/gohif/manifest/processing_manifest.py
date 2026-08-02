from pathlib import Path
import json


class ProcessingManifest:

    def __init__(self, manifest_path):

        self.manifest_path = Path(manifest_path)

        if self.manifest_path.exists():

            with open(self.manifest_path, "r", encoding="utf-8") as f:

                self.completed = set(json.load(f))

        else:

            self.completed = set()

    def is_completed(self, dataset_id):

        return dataset_id in self.completed

    def mark_completed(self, dataset_id):

        self.completed.add(dataset_id)

        self.save()

    def save(self):

        with open(self.manifest_path, "w", encoding="utf-8") as f:

            json.dump(
                sorted(self.completed),
                f,
                indent=2
            )
