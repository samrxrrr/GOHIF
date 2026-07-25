from __future__ import annotations

import asyncio
from pathlib import Path


class DownloadQueue:

    def __init__(self):

        self.queue = asyncio.PriorityQueue()

    async def put(
        self,
        priority: int,
        manifest: Path,
    ):

        await self.queue.put(
            (
                priority,
                manifest,
            )
        )

    async def get(self):

        return await self.queue.get()

    def empty(self):

        return self.queue.empty()

    def task_done(self):

        self.queue.task_done()
