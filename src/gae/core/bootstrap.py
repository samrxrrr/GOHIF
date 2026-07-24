from gae.plugins.http.plugin import HTTPPlugin
from gae.registry.plugin_registry import PluginRegistry


def bootstrap():

    registry = PluginRegistry()

    registry.register(
        "http",
        HTTPPlugin,
    )

    registry.register(
        "https",
        HTTPPlugin,
    )

    return registry
