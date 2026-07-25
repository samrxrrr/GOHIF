from importlib import import_module
from pathlib import Path

from gae.registry.plugin_registry import PluginRegistry
from gae.interfaces.plugin import AcquisitionPlugin


def discover_plugins(registry: PluginRegistry):

    plugins_dir = Path(__file__).resolve().parent.parent / "plugins"

    for directory in plugins_dir.iterdir():

        if not directory.is_dir():
            continue

        if directory.name.startswith("__"):
            continue

        try:

            module = import_module(
                f"gae.plugins.{directory.name}.plugin"
            )

            plugin = module.__dict__.values()

            for obj in plugin:

                if (
                    isinstance(obj, type)
                    and issubclass(obj, AcquisitionPlugin)
                    and obj is not AcquisitionPlugin
                ):

                    instance = obj()

                    registry.register(
                        instance.name,
                        obj,
                    )

        except Exception as e:

            print(
                f"Skipping {directory.name}: {e}"
            )
