from pathlib import Path
import json

from gohif.artifacts.artifact import Artifact


class ArtifactRegistry:

    def __init__(self):

        self.output = Path("/mnt/g/My Drive/DATASETS/_artifacts")

        self.output.mkdir(exist_ok=True)

    def save(self, artifact: Artifact):

        outfile = self.output / f"{artifact.artifact_id}.json"

        with open(outfile, "w", encoding="utf-8") as f:

            json.dump(
                artifact.__dict__,
                f,
                indent=2
            )

        return outfile
