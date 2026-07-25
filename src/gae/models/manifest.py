from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, HttpUrl


class Checksum(BaseModel):
    algorithm: Literal["md5", "sha1", "sha256", "sha512"]
    value: str


class Download(BaseModel):

    method: Literal[
        "http",
        "https",
        "ftp",
        "rest",
        "graphql",
        "github",
        "bitbucket",
        "zenodo",
        "figshare",
        "kaggle",
        "aws",
        "ncbi",
        "ena",
        "browser",
    ]

    # Generic URL-based protocols
    url: HttpUrl | None = None

    # NCBI / ENA / SRA / GEO
    database: str | None = None
    accession: str | None = None

    # NCBI Entrez
    email: str | None = None
    api_key: str | None = None

    # Kaggle
    dataset: str | None = None

    # Zenodo / Figshare
    doi: str | None = None
    record_id: str | None = None


class Storage(BaseModel):
    output_directory: str
    filename: str | None = None


class Dataset(BaseModel):
    id: str
    name: str
    domain: str
    version: str
    description: str | None = None
    license: str | None = None


class Manifest(BaseModel):
    dataset: Dataset
    download: Download
    storage: Storage
    checksum: Checksum | None = None
