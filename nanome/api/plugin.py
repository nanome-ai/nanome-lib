from . import _DefaultPlugin
from nanome._internal import _network as Network, _Plugin, _PluginInstance
from nanome._internal._process import _ProcessManager
from nanome._internal._network._serialization._serializer import Serializer
from nanome.util.logs import Logs
from nanome.util import config
from multiprocessing import Process, Pipe
import sys
import json
import cProfile

class Plugin(_Plugin):
    """
    | Core class of any Plugin.
    | Manages network, callbacks and APIs

    :param name: Name of the plugin to display
    :type name: :class:`str`
    :param description: Description of the plugin to display
    :type description: :class:`str`
    :param tags: Tags of the plugin
    :type tags: :class:`list` <:class:`str`>
    :param has_advanced: If true, plugin will display an "Advanced Settings" button
    :type has_advanced: :class:`bool`
    """
    @classmethod
    def setup(cls, name, description, tags, has_advanced, plugin_class, host = "config", port = "config", key = "config", permissions=[], integrations=[]):
        if not _Plugin._is_process():
            plugin = cls(name, description, tags, has_advanced, permissions, integrations)
            plugin.set_plugin_class(plugin_class)
            plugin.run(host, port, key)

    @staticmethod
    def set_custom_data(*args):
        """
        | Store arbitrary data to send to plugin instances

        :param args: Variable length argument list
        :type args: Anything serializable
        """
        _Plugin._custom_data = args

    @staticmethod
    def set_maximum_processes_count(max_process_nb):
        _ProcessManager._max_process_count = max_process_nb

    def run(self, host = "config", port = "config", key = "config"):
        """
        | Starts the plugin by connecting to the server specified.
        | If arguments (-a, -p) are given when starting plugin, host/port will be ignored.
        | Function will return only when plugin exits.

        :param host: NTS IP address if plugin started without -a option
        :param port: NTS port if plugin started without -p option
        :type host: str
        :type port: int
        """
        if (host == "config"):
            self.__host = config.fetch("host")
        else:
            self.__host = host
        if (port == "config"):
            self.__port = config.fetch("port")
        else:
            self.__port = port
        if (key == "config"):
            self.__key = config.fetch("key")
        else:
            self.__key = key
        self.__parse_args()
        Logs.debug("Start plugin")
        if self.__has_autoreload:
            self.__autoreload()
        else:
            self.__run()

    def set_plugin_class(self, plugin_class):
        """
        | Set plugin class to instantiate when a new session is connected
        | The plugin class should interact with or override functions in :class:`~nanome.PluginInstance` to interact with Nanome

        :param plugin_class: Plugin class to instantiate
        :type plugin_class: :class:`~nanome.PluginInstance`
        """
        self._plugin_class = plugin_class

    @property
    def pre_run(self):
        """
        | Function to call before the plugin runs and tries to connect to NTS
        | Useful when using autoreload
        """
        return self._pre_run
    @pre_run.setter
    def pre_run(self, value):
        self._pre_run = value

    @property
    def post_run(self):
        """
        | Function to call when the plugin is about to exit
        | Useful when using autoreload
        """
        return self._post_run
    @post_run.setter
    def post_run(self, value):
        self._post_run = value

    def __init__(self, name, description, tags=[], has_advanced = False, permissions=[], integrations=[]):
        super(Plugin, self).__init__(name, description, tags, has_advanced, permissions, integrations)
        self._plugin_class = _DefaultPlugin
