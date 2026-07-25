from gae.registry.plugin_registry import PluginRegistry
from gae.core.plugin_loader import discover_plugins


def bootstrap():

    registry = PluginRegistry()

    discover_plugins(registry)

    return registry
