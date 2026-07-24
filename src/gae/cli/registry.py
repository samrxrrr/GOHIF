from __future__ import annotations

import asyncio

from gae.executor.parallel import ParallelExecutor
from gae.plugins.http.plugin import HTTPPlugin
from gae.registry.dataset_registry import DatasetRegistry
from gae.registry.plugin_registry import PluginRegistry


async def main():

    registry = PluginRegistry()

    registry.register(
        "http",
        HTTPPlugin,
    )

    datasets = DatasetRegistry(
        registry_file="registry/datasets.csv",
    )

    executor = ParallelExecutor(
        registry,
        workers=4,
    )

    results = await executor.execute(
        datasets.manifests()
    )

    successful = sum(
        1
        for r in results
        if r["success"]
    )

    failed = len(results) - successful

    print()

    print("========================================")
    print("GOHIF DATASET REGISTRY")
    print("========================================")
    print(f"Datasets : {len(results)}")
    print(f"Success  : {successful}")
    print(f"Failed   : {failed}")
    print("========================================")


if __name__ == "__main__":
    asyncio.run(main())
