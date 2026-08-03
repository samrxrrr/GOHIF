from pathlib import Path
from gohif.artifact.artifact import Artifact
from gohif.artifact.registry import Registry


class ArtifactManager:

    def __init__(self):

        self.root = Path("analysis/results")

        self.registry = Registry(
            self.root / "registry"
        )

    def save(
        self,
        dataframe,
        name,
        phase,
        artifact_type="table"
    ):

        phase_dir = self.root / f"phase{phase}"

        artifact = Artifact(

            name=name,

            phase=str(phase),

            artifact_type=artifact_type

        )

        artifact.save(
            dataframe,
            phase_dir
        )

        self.registry.register(
            phase_dir /
            f"{name}.metadata.json"
        )

        print(
            f"[GOHIF] Registered artifact: {name}"
        )
