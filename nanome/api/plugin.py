import sys

from . import _DefaultPlugin
from nanome._internal import _Plugin
from nanome._internal.logs import LogsManager
from nanome._internal._process import ProcessManager
from nanome.util.logs import Logs
from nanome.util import config


class Plugin(_Plugin):
    """Process that connects to NTS, and allows a user to access a PluginInstance.

    When plugin process is running, an entry is added to the Nanome Stacks Menu.

    When a user activates a Plugin, this class creates a PluginInstance object
    connected to the user's Nanome session.
    """

    def __init__(self, name, description, tags=None, has_advanced=False, permissions=None, integrations=None, version=None):
        """
        :param name: Name of the plugin to display
        :type name: :class:`str`
        :param description: Description of the plugin to display
        :type description: :class:`str`
        :param tags: Tags of the plugin
        :type tags: :class:`list` <:class:`str`>
        :param has_advanced: If true, plugin will display an "Advanced Settings" button
        :type has_advanced: :class:`bool`
        :param version: Semantic version number of plugin. Used for logging.
        :type version: :class:`str`
        """
        tags = tags or []
        permissions = permissions or []
        integrations = integrations or []
        super(Plugin, self).__init__(
            name, description, tags=tags, has_advanced=has_advanced,
            permissions=permissions, integrations=integrations)
        self.plugin_class = _DefaultPlugin
        self.version = version

    @staticmethod
    def create_parser():
        """Command Line Interface for Plugins.

        Moved into config.py, but there are plugins that retrieve parser from Plugin class.
        Leaving this here for backwards compatibility.

        rtype: argsparser: args parser
        """
        return config.create_parser()

    def run(self, host=None, port=None, key=None):
        """
        | Starts the plugin by connecting to the server specified.
        | If arguments (-a, -p) are given when starting plugin, host/port will be ignored.
        | Function will return only when plugin exits.

        :param host: NTS IP address if plugin started without -a option
        :param port: NTS port if plugin started without -p option
        :type host: str
        :type port: int
        """
        settings = config.load_settings()
        self.host = host if host else settings.get('host')

        if not self.host:
            Logs.error('No NTS host provided')
            sys.exit(1)
        try:
            self.port = int(port) if port else int(settings.get('port'))
        except ValueError:
            Logs.error('Port must be an integer, received \"{}\"'.format(port))
            sys.exit(1)
        self.key = key if key is not None else settings.get('key')
        self.write_log_file = settings.get('write_log_file') or False
        self.remote_logging = settings.get('remote_logging') or False
        self.has_autoreload = settings.get('auto_reload')
        self.verbose = settings.get('verbose')

        if settings.get('ignore'):
            to_ignore = settings.get('ignore').split(",")
            self.to_ignore = to_ignore

        # Name can be set during the class instantiation without cli arg.
        if settings.get('name'):
            self.name = settings.get('name')

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
    def setup(cls, name, description, tags, has_advanced, plugin_class, host=None,
              port=None, key=None, permissions=None, integrations=None):
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
        ProcessManager._max_process_count = max_process_nb

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
