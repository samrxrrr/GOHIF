from __future__ import annotations

import asyncio
from aiolimiter import AsyncLimiter


class DownloadScheduler:

    def __init__(
        self,
        workers=4,
        rate_limit=8,
    ):

        self.semaphore = asyncio.Semaphore(workers)

        self.limiter = AsyncLimiter(
            rate_limit,
            1,
        )

    async def acquire(self):

        async with self.semaphore:

            async with self.limiter:

                yield
