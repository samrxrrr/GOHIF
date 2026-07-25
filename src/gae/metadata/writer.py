from pathlib import Path
import json

from gae.models.metadata import DatasetMetadata


def write_metadata(metadata: DatasetMetadata, destination: Path):

    outfile = destination.with_suffix(".metadata.json")

    outfile.write_text(
        json.dumps(
            metadata.model_dump(),
            indent=4,
            default=str,
        )
    )

    return outfile
