from . import _DefaultPlugin
from nanome._internal import _network as Network, _Plugin, _PluginInstance
from nanome._internal._network._serialization._serializer import Serializer
from nanome.util.logs import Logs
from multiprocessing import Process, Pipe
import sys
import json
import cProfile

class Plugin(_Plugin):
    """
    | Core class of any Plugin.
    | Manages network, callbacks and APIs

    :param name: Name of the plugin to display
    :param description: Description of the plugin to display
    :param category: Category of the plugin
    :param has_advanced: If true, plugin will display an "Advanced Settings" button
    :type name: str
    :type description: str
    :type category: str
    :type has_advanced: bool
    """
    def run(self, host = '127.0.0.1', port = 8888, key_file = "nts_key"):
        """
        | Starts the plugin by connecting to the server specified.
        | If arguments (-a, -p) are given when starting plugin, host/port will be ignored.
        | Function will return only when plugin exits.

        :param host: NTS IP address if plugin started without -a option
        :param port: NTS port if plugin started without -p option
        :type host: str
        :type port: int
        """
        self.__host = host
        self.__port = port
        self.__key_file = key_file
        self.__parse_args()
        Logs.debug("Start plugin")
        self.__run()

    def set_plugin_class(self, plugin_class):
        """
        | Set plugin class to instantiate when a new session is connected
        | If using a custom class, functions in :func:~nanome.api.plugin_instance._PluginInstance can be overriden

        :param plugin_class: Plugin class to instantiate
        :type plugin_class: :class:`~nanome.api.plugin_instance.PluginInstance`
        """
        self._plugin_class = plugin_class

    def __init__(self, name, description, category = "", has_advanced = False):
        super(Plugin, self).__init__(name, description, category, has_advanced)
        self._plugin_class = _DefaultPlugin
