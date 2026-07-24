from __future__ import annotations

from gae.acquisition.job import AcquisitionJob
from gae.acquisition.pipeline import AcquisitionPipeline


class AcquisitionManager:

    def __init__(self):

        self.pipeline = AcquisitionPipeline()

    async def start(
        self,
        job: AcquisitionJob,
    ):

        await self.pipeline.before_prepare(job)

        job.status = "PREPARING"

        await self.pipeline.after_prepare(job)

        await self.pipeline.before_download(job)

        job.status = "DOWNLOADING"

        await self.pipeline.after_download(job)

        await self.pipeline.before_validation(job)

        job.status = "VALIDATING"

        await self.pipeline.after_validation(job)

        await self.pipeline.before_finish(job)

        job.status = "FINISHED"

        await self.pipeline.after_finish(job)

        return job
