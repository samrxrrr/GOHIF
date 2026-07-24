from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from uuid import uuid4


@dataclass
class AcquisitionJob:

    dataset_id: str

    dataset_name: str

    plugin: str

    source_url: str

    destination: Path

    job_id: str = field(default_factory=lambda: str(uuid4()))

    created_at: datetime = field(default_factory=datetime.utcnow)

    started_at: datetime | None = None

    finished_at: datetime | None = None

    status: str = "PENDING"

    error: str | None = None
