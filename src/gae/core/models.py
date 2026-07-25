from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class Dataset(BaseModel):

    id: str
    name: str
    domain: str
    version: str
    description: Optional[str] = None
    license: Optional[str] = None


class Download(BaseModel):

    method: str

    url: Optional[str] = None

    database: Optional[str] = None

    accession: Optional[str] = None

    email: Optional[str] = None


class Storage(BaseModel):

    output_directory: Path

    filename: Optional[str] = None


class Manifest(BaseModel):

    dataset: Dataset

    download: Download

    storage: Storage

    checksum: Optional[str] = None
