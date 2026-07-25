from gae.registry.plugin_registry import PluginRegistry

from gae.plugins.http.plugin import HTTPPlugin
from gae.plugins.ftp.plugin import FTPPlugin
from gae.plugins.ncbi.plugin import NCBIPlugin
from gae.plugins.ena.plugin import ENAPlugin


def bootstrap():

    registry = PluginRegistry()

    registry.register("http", HTTPPlugin)
    registry.register("https", HTTPPlugin)
    registry.register("ftp", FTPPlugin)
    registry.register("ncbi", NCBIPlugin)
    registry.register("ena", ENAPlugin)

    return registry
