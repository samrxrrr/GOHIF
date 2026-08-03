from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import hashlib
import json
import pandas as pd


@dataclass
class Artifact:

    name: str
    phase: str
    artifact_type: str
    version: str = "1.0.0"

    def save(self, dataframe: pd.DataFrame, output_dir: str):

        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        csv_path = out / f"{self.name}.csv"

        dataframe.to_csv(csv_path, index=False)

        checksum = hashlib.sha256(
            csv_path.read_bytes()
        ).hexdigest()

        metadata = asdict(self)

        metadata["created"] = datetime.now().isoformat()

        metadata["rows"] = len(dataframe)

        metadata["columns"] = list(dataframe.columns)

        metadata["sha256"] = checksum

        with open(
            out / f"{self.name}.metadata.json",
            "w"
        ) as f:

            json.dump(metadata, f, indent=4)

        return csv_path
