from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, HttpUrl, model_validator


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

    url: HttpUrl | None = None

    database: str | None = None

    accession: str | None = None

    email: str | None = None

    api_key: str | None = None

    dataset: str | None = None

    doi: str | None = None

    record_id: str | None = None

    @model_validator(mode="after")
    def validate_protocol(self):

        if self.method in {
            "http",
            "https",
            "ftp",
            "rest",
            "graphql",
            "github",
            "bitbucket",
            "browser",
        }:

            if self.url is None:
                raise ValueError(
                    f"{self.method} requires download.url"
                )

        if self.method == "ncbi":

            if self.database is None:
                raise ValueError(
                    "NCBI requires download.database"
                )

            if self.accession is None:
                raise ValueError(
                    "NCBI requires download.accession"
                )

        if self.method == "ena":

            if self.accession is None:
                raise ValueError(
                    "ENA requires download.accession"
                )

        return self


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
