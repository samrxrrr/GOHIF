from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from gae.executor.parallel import ParallelExecutor
from gae.registry.plugin_registry import PluginRegistry
from gae.plugins.http.plugin import HTTPPlugin


async def main():

    registry = PluginRegistry()

    registry.register(
        "http",
        HTTPPlugin,
    )

    manifests = [
        Path(x)
        for x in sys.argv[1:]
    ]

    executor = ParallelExecutor(
        registry,
        workers=4,
    )

    results = await executor.execute(
        manifests
    )

    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
