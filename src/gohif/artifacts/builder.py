from pathlib import Path
import json
import uuid

from gohif.artifacts.artifact import Artifact
from gohif.artifacts.registry import ArtifactRegistry


INPUT = Path("/mnt/g/My Drive/DATASETS/_metadata_semantic")


class ArtifactBuilder:

    def __init__(self):

        self.registry = ArtifactRegistry()

    def build(self, metadata_file):

        with open(metadata_file, encoding="utf-8") as f:

            meta = json.load(f)

        artifact = Artifact(

            artifact_id=str(uuid.uuid4()),

            dataset_id=meta["dataset_id"],

            artifact_type=meta["dataset_type"],

            source_file=meta["dataset_path"]

        )

        artifact.metadata = meta

        artifact.content["title"] = meta.get("title","")

        artifact.entities["genes"] = meta.get("genes",[])

        artifact.entities["proteins"] = meta.get("proteins",[])

        artifact.entities["species"] = meta.get("organisms",[])

        artifact.entities["diseases"] = meta.get("diseases",[])

        artifact.entities["pathogens"] = meta.get("pathogens",[])

        artifact.entities["countries"] = meta.get("countries",[])

        self.registry.save(artifact)


builder = ArtifactBuilder()

count = 0

for file in sorted(INPUT.glob("GOHIF_DS_*.json")):

    builder.build(file)

    count += 1

print("="*70)
print("Artifacts Built :",count)
print("="*70)
