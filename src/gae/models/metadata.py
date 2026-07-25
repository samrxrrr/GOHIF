from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class DatasetMetadata(BaseModel):

    repository: str

    dataset_id: str

    title: str

    version: str | None = None

    doi: str | None = None

    accession: str | None = None

    citation: str | None = None

    license: str | None = None

    source_url: str | None = None

    checksum: str | None = None

    file_size: int | None = None

    downloaded_at: datetime = datetime.utcnow()

    extra: dict = {}
