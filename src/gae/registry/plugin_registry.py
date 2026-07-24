from __future__ import annotations

from typing import Dict, Type

from gae.interfaces.plugin import AcquisitionPlugin


class PluginRegistry:

    def __init__(self) -> None:
        self._plugins: Dict[str, Type[AcquisitionPlugin]] = {}

    def register(
        self,
        name: str,
        plugin: Type[AcquisitionPlugin],
    ) -> None:
        self._plugins[name.lower()] = plugin

    def get(
        self,
        name: str,
    ) -> Type[AcquisitionPlugin]:

        try:
            return self._plugins[name.lower()]
        except KeyError:
            raise ValueError(f"Unknown plugin: {name}")

    def available(self) -> list[str]:
        return sorted(self._plugins.keys())
