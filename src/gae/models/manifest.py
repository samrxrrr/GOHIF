from pydantic import BaseModel, HttpUrl
from typing import Literal


class Manifest(BaseModel):

    dataset_id: str

    dataset_name: str

    domain: str

    version: str

    acquisition_method: Literal[
        "http",
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

    output_directory: str

    expected_extension: str

    checksum: str | None = None

    license: str | None = None
