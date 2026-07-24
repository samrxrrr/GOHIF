from __future__ import annotations

from pathlib import Path
from datetime import datetime

from gae.acquisition.job import AcquisitionJob
from gae.acquisition.manager import AcquisitionManager
from gae.core.application import load_manifest
from gae.core.database import Database
from gae.core.logger import setup_logger
from gae.download.checksum import calculate_checksum
from gae.registry.plugin_registry import PluginRegistry


class Controller:

    def __init__(self, registry: PluginRegistry):

        self.registry = registry
        self.logger = setup_logger()
        self.database = Database()
        self.manager = AcquisitionManager()

    async def run(self, manifest_path: Path):

        started = datetime.utcnow()

        manifest = load_manifest(manifest_path)

        plugin_cls = self.registry.get(
            manifest.download.method
        )

        plugin = plugin_cls()

        filename = (
            manifest.storage.filename
            or Path(str(manifest.download.url)).name
        )

        destination = (
            Path(manifest.storage.output_directory)
            / filename
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        job = AcquisitionJob(
            dataset_id=manifest.dataset.id,
            dataset_name=manifest.dataset.name,
            plugin=plugin.name,
            source_url=str(manifest.download.url),
            destination=destination,
        )

        downloaded, verified, metadata = await self.manager.execute(
            job=job,
            plugin=plugin,
            manifest=manifest,
        )

        sha256 = calculate_checksum(
            downloaded,
            "sha256",
        )

        finished = datetime.utcnow()

        duration = (
            finished - started
        ).total_seconds()

        self.database.insert(
            (
                manifest.dataset.id,
                manifest.dataset.name,
                manifest.dataset.version,
                plugin.name,
                str(manifest.download.url),
                str(downloaded),
                metadata["size"],
                sha256,
                job.status,
                started.isoformat(),
                finished.isoformat(),
                duration,
                job.error or "",
            )
        )

        self.database.close()

        return {
            "job_id": job.job_id,
            "status": job.status,
            "success": verified,
            "file": str(downloaded),
            "metadata": metadata,
            "sha256": sha256,
        }
