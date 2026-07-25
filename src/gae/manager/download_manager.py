from __future__ import annotations

import asyncio
import csv
from pathlib import Path

from gae.core.controller import Controller
from gae.queue.download_queue import DownloadQueue
from gae.registry.plugin_registry import PluginRegistry


class DownloadManager:

    def __init__(
        self,
        registry: PluginRegistry,
        workers: int = 4,
    ):

        self.registry = registry
        self.workers = workers
        self.queue = DownloadQueue()

    async def worker(self):

        controller = Controller(
            self.registry
        )

        while True:

            priority,manifest = await self.queue.get()

            try:

                await controller.run(
                    manifest
                )

            except Exception as e:

                print(e)

            self.queue.task_done()

    async def run_registry(
        self,
        registry_csv,
    ):

        with open(registry_csv) as f:

            reader = csv.DictReader(f)

            for row in reader:

                if row["enabled"].lower()!="true":
                    continue

                await self.queue.put(
                    int(row["priority"]),
                    Path(row["manifest"]),
                )

        workers=[]

        for _ in range(self.workers):

            task=asyncio.create_task(
                self.worker()
            )

            workers.append(task)

        await self.queue.queue.join()

        for task in workers:

            task.cancel()
