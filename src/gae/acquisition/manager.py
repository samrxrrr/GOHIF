from __future__ import annotations

from datetime import datetime

from gae.acquisition.job import AcquisitionJob
from gae.acquisition.pipeline import AcquisitionPipeline


class AcquisitionManager:

    def __init__(self):
        self.pipeline = AcquisitionPipeline()

    async def execute(
        self,
        job: AcquisitionJob,
        plugin,
        manifest,
    ):

        job.started_at = datetime.utcnow()
        job.status = "PREPARING"

        await self.pipeline.before_prepare(job)
        await plugin.prepare(manifest)
        await plugin.authenticate()
        await self.pipeline.after_prepare(job)

        job.status = "DOWNLOADING"

        await self.pipeline.before_download(job)

        downloaded = await plugin.acquire(
            manifest,
            job.destination,
        )

        await self.pipeline.after_download(job)

        job.status = "VALIDATING"

        await self.pipeline.before_validation(job)

        verified = await plugin.verify(downloaded)

        metadata = await plugin.metadata(downloaded)

        await plugin.cleanup()

        await self.pipeline.after_validation(job)

        job.finished_at = datetime.utcnow()

        job.status = "SUCCESS" if verified else "FAILED"

        await self.pipeline.before_finish(job)
        await self.pipeline.after_finish(job)

        return downloaded, verified, metadata
