"""
Configuration models.

These Pydantic models define the canonical configuration schema used
throughout GOHIF.
"""

from __future__ import annotations

from pydantic import BaseModel


class ProjectConfig(BaseModel):

    name: str

    version: str

    author: str


class LoggingConfig(BaseModel):

    level: str

    directory: str


class StorageConfig(BaseModel):

    data_directory: str

    output_directory: str

    database: str

    database_file: str


class RuntimeConfig(BaseModel):

    environment: str

    threads: int

    random_seed: int
