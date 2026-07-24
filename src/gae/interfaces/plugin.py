from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class AcquisitionPlugin(ABC):
    """
    Base interface implemented by every acquisition plugin.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    async def prepare(self, manifest: dict[str, Any]) -> None:
        ...

    @abstractmethod
    async def authenticate(self) -> None:
        ...

    @abstractmethod
    async def acquire(
        self,
        manifest: dict[str, Any],
        destination: Path,
    ) -> Path:
        ...

    @abstractmethod
    async def verify(self, downloaded_file: Path) -> bool:
        ...

    @abstractmethod
    async def metadata(self, downloaded_file: Path) -> dict[str, Any]:
        ...

    @abstractmethod
    async def cleanup(self) -> None:
        ...
