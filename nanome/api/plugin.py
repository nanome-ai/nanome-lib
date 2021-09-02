import argparse

from . import _DefaultPlugin
from nanome._internal import _Plugin
from nanome._internal._process import _ProcessManager
from nanome.util.logs import Logs
from nanome.util import config


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

    @staticmethod
    def create_parser():
        """Command Line Interface for Plugins.

        rtype: argsparser: args parser
        """
        parser = argparse.ArgumentParser(description='Starts a Nanome Plugin.')
        parser.add_argument('-a', '--host', help='connects to NTS at the specified IP address')
        parser.add_argument('-p', '--port', type=int, help='connects to NTS at the specified port')
        parser.add_argument('-r', '--auto-reload', action='store_true', help='Restart plugin automatically if a .py or .json file in current directory changes')
        parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose mode, to display Logs.debug')
        parser.add_argument('-n', '--name', help='Name to display for this plugin in Nanome', default='')
        parser.add_argument('-k', '--keyfile', default='', help='Specifies a key file or key string to use to connect to NTS')
        parser.add_argument('-i', '--ignore', help='To use with auto-reload. All paths matching this pattern will be ignored, use commas to specify several. Supports */?/[seq]/[!seq]', default='')
        parser.add_argument('--write-log-file', type=bool, help='Enable or disable writing logs to .log file')
        return parser

    @classmethod
    def setup(cls, name, description, tags, has_advanced, plugin_class, host="config", port="config", key="config", permissions=[], integrations=[]):
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

    def run(self, host="config", port="config", key="config"):
        """
        | Starts the plugin by connecting to the server specified.
        | If arguments (-a, -p) are given when starting plugin, host/port will be ignored.
        | Function will return only when plugin exits.

        :param host: NTS IP address if plugin started without -a option
        :param port: NTS port if plugin started without -p option
        :type host: str
        :type port: int
        """
        default_host = config.fetch('host') if host == 'config' else host
        default_port = config.fetch('port') if port == 'config' else port
        default_key = config.fetch('key') if key == 'config' else key
        default_write_log_file = config.fetch('write_log_file')

        # Parse command line args and set internal variables.
        parser = self.create_parser()
        args, _ = parser.parse_known_args()

        self.__host = args.host or default_host
        self.__port = args.port or default_port
        self.__key = args.keyfile or default_key

        if args.write_log_file is not None:
            self.__write_log_file = args.write_log_file
        else:
            self.__write_log_file = default_write_log_file

        self.__has_autoreload = args.auto_reload
        self.__has_verbose = args.verbose
        Logs._set_verbose(args.verbose)

        if args.ignore:
            to_ignore = args.ignore.split(",")
            self.__to_ignore.extend(to_ignore)

        # Name can be set during the class instantiation without cli arg.
        if args.name:
            self._description['name'] = args.name

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

    def __init__(self, name, description, tags=[], has_advanced=False, permissions=[], integrations=[]):
        super(Plugin, self).__init__(name, description, tags, has_advanced, permissions, integrations)
        self._plugin_class = _DefaultPlugin
