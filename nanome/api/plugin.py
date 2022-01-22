import argparse
import os

from . import _DefaultPlugin
from nanome._internal import _Plugin
from nanome._internal.logs import LogsManager
from nanome._internal._process import _ProcessManager
from nanome.util.logs import Logs
from nanome.util import config


def str2bool(v):
    """Accept various truthy/falsey values as boolean arguments."""
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class Plugin(_Plugin):
    """Process that connects to NTS, and allows a user to access a PluginInstance.

    When plugin process is running, an entry is added to the Nanome Stacks Menu.

    When a user activates a Plugin, this class creates a PluginInstance object
    connected to the user's Nanome session.
    """

    def __init__(self, name, description, tags=None, has_advanced=False, permissions=None, integrations=None):
        """
        :param name: Name of the plugin to display
        :type name: :class:`str`
        :param description: Description of the plugin to display
        :type description: :class:`str`
        :param tags: Tags of the plugin
        :type tags: :class:`list` <:class:`str`>
        :param has_advanced: If true, plugin will display an "Advanced Settings" button
        :type has_advanced: :class:`bool`
        """
        tags = tags or []
        permissions = permissions or []
        integrations = integrations or []
        super(Plugin, self).__init__(
            name, description, tags=tags, has_advanced=has_advanced,
            permissions=permissions, integrations=integrations)
        self.plugin_class = _DefaultPlugin

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
        parser.add_argument('--write-log-file', type=str2bool, help='Enable or disable writing logs to .log file')
        parser.add_argument('--remote-logging', type=str2bool, dest='remote_logging', help='Toggle whether or not logs should be forwarded to NTS.')
        return parser

    @property
    def environ_dict(self):
        """Get values set by environment variables."""
        environ_dict = {
            'host': os.environ.get('NTS_HOST'),
            'port': os.environ.get('NTS_PORT'),
            'key': os.environ.get('NTS_KEYFILE'),
            'auto-reload': os.environ.get('PLUGIN_AUTO_RELOAD'),
            'name': os.environ.get('PLUGIN_NAME'),
            'verbose': os.environ.get('PLUGIN_VERBOSE'),
            'write-log-file': os.environ.get('PLUGIN_WRITE_LOG_FILE'),
            'remote-logging': os.environ.get('PLUGIN_REMOTE_LOGGING'),
        }
        # remove any keys that haven't been set.
        environ_dict = {k: v for k, v in environ_dict.items() if v is not None}
        return environ_dict

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
        # Order of priority for settings:
        # 1. First, parameters to function are checked
        # 2) Then CLI args are checked.
        # 3) Then Environment variables.
        # 4) then nanome json config file

        # Parse command line args and set internal variables.
        parser = self.create_parser()
        cli_dict = vars(parser.parse_known_args()[0])
        for k in list(cli_dict.keys()):
            if cli_dict[k] in ['config', None, '']:
                cli_dict.pop(k)
        environ_dict = self.environ_dict

        # Create dict out of config file.
        config_file_dict = {
            "host": config.fetch("host"),
            "port": config.fetch("port"),
            "key": config.fetch("key"),
            "plugin_files_path": config.fetch("plugin_files_path"),
            "write_log_file": config.fetch("write_log_file"),
        }

        fn_params = {'host': host, 'port': port, 'key': key}
        for k in list(fn_params):
            if fn_params[k] == 'config':
                fn_params.pop(k)

        plugin_settings = {**config_file_dict, **environ_dict, **cli_dict, **fn_params}

        self.host = plugin_settings.get('host')
        self.port = int(plugin_settings.get('port'))
        self.key = plugin_settings.get('key')
        self.write_log_file = plugin_settings.get('write_log_file') or False
        self.remote_logging = plugin_settings.get('remote_logging') or False
        self.has_autoreload = plugin_settings.get('auto_reload')
        self.verbose = plugin_settings.get('verbose')

        if plugin_settings.get('ignore'):
            to_ignore = plugin_settings.get('ignore').split(",")
            self.to_ignore = to_ignore

        # Name can be set during the class instantiation without cli arg.
        if plugin_settings.get('name'):
            self.name = plugin_settings.get('name')

        # Configure Logging
        self.__log_filename = self._plugin_class.__name__ + ".log"
        self._logs_manager = LogsManager(
            self.__log_filename,
            plugin=self,
            write_log_file=self.write_log_file,
            remote_logging=self.remote_logging)
        self._logs_manager.configure_main_process(self.plugin_class)

        Logs.message("Starting Plugin")

        if self.has_autoreload:
            self._autoreload()
        else:
            self._run()

    @classmethod
    def setup(cls, name, description, tags, has_advanced, plugin_class, host="config",
              port="config", key="config", permissions=None, integrations=None):

        permissions = permissions or []
        integrations = integrations or []
        if not cls._is_process():
            plugin = cls(name, description, tags, has_advanced, permissions, integrations)
            plugin.plugin_class = plugin_class
            plugin.run(host, port, key)

    def set_custom_data(self, *args):
        """
        | Store arbitrary data to send to plugin instances

        :param args: Variable length argument list
        :type args: Anything serializable
        """
        self._custom_data = args

    @staticmethod
    def set_maximum_processes_count(max_process_nb):
        _ProcessManager._max_process_count = max_process_nb

    @property
    def host(self):
        return getattr(self, '_host', None)

    @host.setter
    def host(self, value):
        setattr(self, '_host', value)

    @property
    def port(self):
        return getattr(self, '_port', None)

    @port.setter
    def port(self, value):
        setattr(self, '_port', value)

    @property
    def key(self):
        return getattr(self, '_key', None)

    @key.setter
    def key(self, value):
        setattr(self, '_key', value)

    @property
    def write_log_file(self):
        return getattr(self, '_write_log_file', None)

    @write_log_file.setter
    def write_log_file(self, value):
        setattr(self, '_write_log_file', value)

    @property
    def remote_logging(self):
        return getattr(self, '_remote_logging', None)

    @remote_logging.setter
    def remote_logging(self, value):
        setattr(self, '_remote_logging', value)

    @property
    def verbose(self):
        return getattr(self, '_verbose', None)

    @verbose.setter
    def verbose(self, value):
        setattr(self, '_verbose', value)

    @property
    def has_autoreload(self):
        return getattr(self, '_has_autoreload', None)

    @has_autoreload.setter
    def has_autoreload(self, value):
        setattr(self, '_has_autoreload', value)

    @property
    def to_ignore(self):
        return getattr(self, '_to_ignore')

    @to_ignore.setter
    def to_ignore(self, value):
        setattr(self, '_to_ignore', value)

    @property
    def plugin_class(self):
        """Child class of PluginInstance class that will be instantiated when Session activated."""
        return getattr(self, '_plugin_class', None)

    @plugin_class.setter
    def plugin_class(self, value):
        setattr(self, '_plugin_class', value)

    @property
    def name(self):
        """Name of plugin as shown in the Nanome Stacks menu."""
        return self._description.get('name')

    @name.setter
    def name(self, value):
        self._description['name'] = value

    def set_plugin_class(self, plugin_class):
        """
        | Set plugin class to instantiate when a new session is connected
        | The plugin class should interact with or override functions in :class:`~nanome.PluginInstance` to interact with Nanome

        :param plugin_class: Plugin class to instantiate
        :type plugin_class: :class:`~nanome.PluginInstance`
        """
        self.plugin_class = plugin_class

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
