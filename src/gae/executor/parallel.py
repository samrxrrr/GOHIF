from __future__ import annotations

import asyncio

from gae.core.controller import Controller
from gae.registry.plugin_registry import PluginRegistry


class ParallelExecutor:

    def __init__(
        self,
        registry: PluginRegistry,
        workers: int = 4,
    ):
        self.registry = registry
        self.workers = workers
        self.semaphore = asyncio.Semaphore(workers)

    async def _run(self, manifest):

        async with self.semaphore:

            controller = Controller(self.registry)

            return await controller.run(manifest)

    async def execute(
        self,
        manifests,
    ):

        tasks = [
            asyncio.create_task(
                self._run(manifest)
            )
            for manifest in manifests
        ]

        return await asyncio.gather(*tasks)
