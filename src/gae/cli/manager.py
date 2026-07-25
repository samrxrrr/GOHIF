from __future__ import annotations

import asyncio

from gae.manager.download_manager import DownloadManager
from gae.plugins.http.plugin import HTTPPlugin
from gae.registry.plugin_registry import PluginRegistry


async def main():

    registry=PluginRegistry()

    registry.register(
        "http",
        HTTPPlugin,
    )

    manager=DownloadManager(
        registry,
        workers=4,
    )

    await manager.run_registry(
        "registry/datasets.csv"
    )

    print()
    print("===================================")
    print("DOWNLOAD MANAGER FINISHED")
    print("===================================")


if __name__=="__main__":
    asyncio.run(main())
