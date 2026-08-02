from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Artifact:

    artifact_id: str

    dataset_id: str

    artifact_type: str

    source_file: str

    metadata: Dict = field(default_factory=dict)

    content: Dict = field(default_factory=lambda: {

        "title": "",

        "text": "",

        "tables": [],

        "figures": []

    })

    entities: Dict = field(default_factory=lambda: {

        "genes": [],

        "proteins": [],

        "species": [],

        "diseases": [],

        "pathogens": [],

        "countries": []

    })

    evidence: List = field(default_factory=list)
