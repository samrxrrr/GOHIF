from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):

    cache_directory: Path = Path.home() / ".gae_cache"

    log_directory: Path = Path.home() / ".gae_logs"

    database: Path = Path("gae.db")

    workers: int = 4

    chunk_size: int = 1024 * 1024

    timeout: int = 300

    retries: int = 3

    verify_ssl: bool = True


settings = Settings()
