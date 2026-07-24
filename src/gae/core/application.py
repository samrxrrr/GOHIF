from pathlib import Path

import yaml

from gae.models.manifest import Manifest


def load_manifest(path: Path) -> Manifest:

    with open(path, "r", encoding="utf-8") as f:

        data = yaml.safe_load(f)

    return Manifest(**data)
