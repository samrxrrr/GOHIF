from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, HttpUrl, Field


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

    url: HttpUrl


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
