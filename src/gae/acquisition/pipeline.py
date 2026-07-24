from __future__ import annotations

from gae.acquisition.job import AcquisitionJob


class AcquisitionPipeline:

    async def before_prepare(
        self,
        job: AcquisitionJob,
    ):
        return

    async def after_prepare(
        self,
        job: AcquisitionJob,
    ):
        return

    async def before_download(
        self,
        job: AcquisitionJob,
    ):
        return

    async def after_download(
        self,
        job: AcquisitionJob,
    ):
        return

    async def before_validation(
        self,
        job: AcquisitionJob,
    ):
        return

    async def after_validation(
        self,
        job: AcquisitionJob,
    ):
        return

    async def before_finish(
        self,
        job: AcquisitionJob,
    ):
        return

    async def after_finish(
        self,
        job: AcquisitionJob,
    ):
        return
