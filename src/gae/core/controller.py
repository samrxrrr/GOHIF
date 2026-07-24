from pathlib import Path

from gae.core.application import load_manifest
from gae.core.logger import setup_logger
from gae.registry.plugin_registry import PluginRegistry


class Controller:

    def __init__(self, registry: PluginRegistry):
        self.registry = registry
        self.logger = setup_logger()

    async def run(self, manifest_path: Path):

        self.logger.info(f"Loading manifest: {manifest_path}")

        manifest = load_manifest(manifest_path)

        self.logger.info(
            f"Dataset: {manifest.dataset.name}"
        )

        plugin_cls = self.registry.get(
            manifest.download.method
        )

        plugin = plugin_cls()

        self.logger.info(
            f"Plugin selected: {plugin.name}"
        )

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

        self.logger.info(
            f"Downloading to: {destination}"
        )

        downloaded = await plugin.acquire(
            manifest,
            destination,
        )

        verified = await plugin.verify(downloaded)

        metadata = await plugin.metadata(downloaded)

        await plugin.cleanup()

        self.logger.info("Download completed")

        return {
            "success": verified,
            "file": str(downloaded),
            "metadata": metadata,
        }
