from __future__ import annotations

from pathlib import Path
from datetime import datetime

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

    async def run(self, manifest_path: Path):

        started = datetime.utcnow()

        manifest = load_manifest(manifest_path)

        plugin_class = self.registry.get(
            manifest.download.method
        )

        plugin = plugin_class()

        await plugin.prepare(manifest)

        await plugin.authenticate()

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

        downloaded = await plugin.acquire(
            manifest,
            destination,
        )

        verified = await plugin.verify(downloaded)

        metadata = await plugin.metadata(downloaded)

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
                "SUCCESS" if verified else "FAILED",
                started.isoformat(),
                finished.isoformat(),
                duration,
                "",
            )
        )

        self.database.close()

        return {
            "success": verified,
            "file": str(downloaded),
            "metadata": metadata,
            "sha256": sha256,
        }
