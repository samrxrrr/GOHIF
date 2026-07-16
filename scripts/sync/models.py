from dataclasses import dataclass
from pathlib import Path

@dataclass
class Domain:

    name: str
    coverage_dir: Path
    srr_dir: Path
