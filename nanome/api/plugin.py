import fnmatch
import json
import logging
import multiprocessing
import os
import random
import re
import signal
import subprocess
import string
import sys
import time
from timeit import default_timer as timer

from nanome._internal.serializer_fields import TypeSerializer
from nanome._internal.logs import LogsManager
from nanome._internal.process import ProcessManager
from nanome._internal import network
from nanome.api._hashes import Hashes
from nanome.api.serializers import CommandMessageSerializer
from nanome.util.logs import Logs
from nanome.util import config
from . import _DefaultPlugin

logger = logging.getLogger(__name__)


MAX_RECONNECT_WAIT = 20.0
KEEP_ALIVE_TIME_INTERVAL = 60.0
KEEP_ALIVE_TIMEOUT = 15.0


class Plugin(object):
    """Process that connects to NTS, and allows a user to access a PluginInstance.

    When plugin process is running, an entry is added to the Nanome Stacks Menu.

    When a user activates a Plugin, this class creates a PluginInstance object
    connected to the user's Nanome session.
    """

    _serializer = CommandMessageSerializer()
    plugin_id = -1
    custom_data = None

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
        super(Plugin, self).__init__()
        self.host = ''
        self.port = None
        self.key = ''
        self.remote_logging = False
        self.write_log_file = True
        self.verbose = False
        self.has_autoreload = False

        tags = tags or []
        permissions = permissions or []
        integrations = integrations or []
        self.plugin_class = _DefaultPlugin
        self.version = version
        self._sessions = dict()
        self._process_manager = ProcessManager()

        if isinstance(tags, str):
            tags = [tags]

        category = ""
        if len(tags) > 0:
            category = tags[0]

        for i in range(0, len(permissions)):
            permissions[i] = Hashes.PermissionRequestHashes[permissions[i]]

        for i in range(0, len(integrations)):
            integrations[i] = Hashes.IntegrationRequestHashes[integrations[i]]

        self._description = {
            'name': name,
            'description': description,
            'category': category,
            'tags': tags,
            'hasAdvanced': has_advanced,
            'auth': None,
            'permissions': permissions,
            'integrations': integrations
        }
        self.connected = False
        self._to_ignore = []
        self.__waiting_keep_alive = False
        self._pre_run = None
        self._post_run = None

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
        self.__log_filename = self.plugin_class.__name__ + ".log"
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
        self.custom_data = args

    @staticmethod
    def set_maximum_processes_count(max_process_nb):
        ProcessManager._max_process_count = max_process_nb

    @property
    def to_ignore(self):
        return getattr(self, '_to_ignore')

    @to_ignore.setter
    def to_ignore(self, value):
        setattr(self, '_to_ignore', value)

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

    @classmethod
    def _run_plugin_instance(
        cls, plugin_instance_class, session_id, net_queue_in, net_queue_out,
        pm_queue_in, pm_queue_out, log_pipe_conn, serializer, plugin_id,
            version_table, original_version_table, custom_data, permissions):
        """When user activates a plugin, this function is run to begin the new process.

        :arg plugin_instance_class: The Plugininstance class to be instantiated.
        :arg session_id: The session ID registered with NTS.
        :arg net_queue_in: The network input queue.
        :arg net_queue_out: The network output queue.
        :arg pm_queue_in: The process manager input queue.
        :arg pm_queue_out: The process manager output queue.
        :arg log_pipe_conn: The pipe to communicate with the logs manager.
        :arg serializer: The serializer to use to create NTS message payloads.
        :arg plugin_id: The plugin ID registered with NTS.
        :arg version_table: The version table of the plugin, used to setup the serializer.
        :arg original_version_table: The original version table of the plugin, used to setup the serializer.
        :arg custom_data: Arbitrary data that can be passed to each instantiated PluginInstance
        :arg permissions: The permissions of the plugin.
        """
        plugin_instance = plugin_instance_class()
        plugin_network = network.PluginNetwork(
            plugin_instance, session_id, net_queue_in, net_queue_out,
            serializer, plugin_id, version_table)
        plugin_instance._setup(
            session_id, plugin_network, pm_queue_in, pm_queue_out,
            log_pipe_conn, original_version_table, custom_data, permissions)
        LogsManager.configure_child_process(plugin_instance)
        logger.debug("Starting plugin")
        plugin_instance._run()

    def _run(self):
        # set_start_method ensures consistent process behavior between Windows and Linux
        if sys.version_info.major >= 3 and sys.version_info.minor >= 4:
            multiprocessing.set_start_method('spawn', force=True)

        if os.name == "nt":
            signal.signal(signal.SIGBREAK, self.__on_termination_signal)
        else:
            signal.signal(signal.SIGTERM, self.__on_termination_signal)

        if self._pre_run is not None:
            self._pre_run()

        self._description['auth'] = self.__read_key()
        self._process_manager = ProcessManager()

        self.__reconnect_attempt = 0
        self._connect()
        self._loop()

    def _connect(self):
        """Create network Connection to NTS, and start listening for packets."""
        self._network = network.NetInstance(self, self.__class__._on_packet_received)
        if self._network.connect(self.host, self.port):
            if self.plugin_id >= 0:
                plugin_id = self.plugin_id
            else:
                plugin_id = 0
            packet = network.Packet()
            packet.set(0, network.Packet.packet_type_plugin_connection, plugin_id)
            packet.write_string(json.dumps(self._description))
            self._network.send(packet)
            self.connected = True
            self.__reconnect_attempt = 0
            self.__waiting_keep_alive = False
            self.__last_keep_alive = timer()
            for session in self._sessions.values():
                session._net_plugin = self._network
            return True
        else:
            self.__disconnection_time = timer()
            self.__reconnect_attempt += 1
            return False

    def _loop(self):
        to_remove = []
        try:
            while True:
                now = timer()

                if self.connected is False:
                    reconnect_wait = min(2 ** self.__reconnect_attempt, MAX_RECONNECT_WAIT)
                    elapsed = now - self.__disconnection_time
                    if elapsed >= reconnect_wait:
                        logger.info("Trying to reconnect...")
                        if self._connect() is False:
                            if self.__reconnect_attempt == 3:
                                self.__disconnect()
                            continue
                    else:
                        time.sleep(reconnect_wait - elapsed)
                        continue
                if self._network.receive() is False:
                    self.connected = False
                    self.__disconnection_time = timer()
                    self._network.disconnect()
                    continue

                if self.__waiting_keep_alive:
                    if now - self.__last_keep_alive >= KEEP_ALIVE_TIMEOUT:
                        self.connected = False
                        self.__disconnection_time = timer()
                        continue
                elif now - self.__last_keep_alive >= KEEP_ALIVE_TIME_INTERVAL and self.plugin_id >= 0:
                    self.__last_keep_alive = now
                    self.__waiting_keep_alive = True
                    packet = network.Packet()
                    packet.set(self.plugin_id, network.Packet.packet_type_keep_alive, 0)
                    self._network.send(packet)

                del to_remove[:]
                for id, session in self._sessions.items():
                    if session.read_from_plugin() is False:
                        session.close_pipes()
                        to_remove.append(id)
                for id in to_remove:
                    self._sessions[id]._send_disconnection_message(self.plugin_id)
                    del self._sessions[id]
                self._process_manager.update()
        except KeyboardInterrupt:
            self.__exit()

    def _start_session_process(self, session_id, version_table):
        """Setup Queues and networking for PluginInstance, run session process."""
        if session_id in self._sessions:  # If session_id already exists, close it first ()
            logger.info("Closing session ID {} because a new session connected with the same ID".format(session_id))
            self._sessions[session_id].signal_and_close_pipes()

        net_queue_in = multiprocessing.Queue()
        net_queue_out = multiprocessing.Queue()
        pm_queue_in = multiprocessing.Queue()
        pm_queue_out = multiprocessing.Queue()
        session = network.Session(
            session_id, self._network, self._process_manager, self._logs_manager,
            net_queue_in, net_queue_out, pm_queue_in, pm_queue_out)
        permissions = self._description["permissions"]
        log_pipe_conn = self._logs_manager.child_pipe_conn
        process = multiprocessing.Process(
            target=self._run_plugin_instance,
            args=(
                self.plugin_class, session_id, net_queue_in, net_queue_out,
                pm_queue_in, pm_queue_out, log_pipe_conn, self._serializer,
                self.plugin_id, version_table, TypeSerializer.get_version_table(),
                self.custom_data, permissions
            )
        )

        # Appending random string to process name makes tracking unique sessions easier
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        process.name = "Session-{}-{}".format(session_id, random_str)
        process.start()
        session.plugin_process = process
        self._sessions[session_id] = session
        extra = {'session_id': session_id}
        logger.info("Registered new session: {}".format(session_id), extra=extra)

    def _on_packet_received(self, packet):
        """When packet received, identify Packet type, and call appropriate function."""
        if packet.packet_type == network.Packet.packet_type_message_to_plugin:
            session_id = packet.session_id
            # Always look if we're trying to register a session
            #   Fix 5/27/2021 - Jeremie: We need to always check for session registration in order to fix timeout issues
            #   When NTS forces disconnection because of plugin list change, session_id still exists in self._sessions,
            #   even though it was disconnected for Nanome
            if self._serializer.try_register_session(packet.payload) is True:
                received_version_table, _, _ = self._serializer.deserialize_command(packet.payload, None)
                version_table = TypeSerializer.get_best_version_table(received_version_table)
                self.__on_client_connection(session_id, version_table)
                return

            if session_id in self._sessions:
                # packet.decompress()
                self._sessions[session_id]._on_packet_received(packet.payload)
                return

            # Doesn't register? It's an error
            logger.warning("Received a command from an unregistered session {}".format(session_id))

        elif packet.packet_type == network.Packet.packet_type_plugin_connection:
            self.plugin_id = packet.plugin_id
            logger.info("Registered with plugin ID {}\n=======================================\n".format(str(self.plugin_id)))

        elif packet.packet_type == network.Packet.packet_type_plugin_disconnection:
            if self.plugin_id == -1:
                if self._description['auth'] is None:
                    logger.error("Connection refused by NTS. Are you missing a security key file?")
                else:
                    logger.error("Connection refused by NTS. Your security key file might be invalid")
                sys.exit(1)
            else:
                logger.info("Connection ended by NTS")
                sys.exit(0)

        elif packet.packet_type == network.Packet.packet_type_client_disconnection:
            try:
                id = packet.session_id
                self._sessions[id].signal_and_close_pipes()
                del self._sessions[id]
                extra = {'session_id': id}
                logger.info("Session {} disconnected".format(id), extra=extra)
            except Exception:
                pass
        elif packet.packet_type == network.Packet.packet_type_keep_alive:
            self.__waiting_keep_alive = False
        elif packet.packet_type == network.Packet.packet_type_logs_request:
            self.__logs_request(packet)
        else:
            logger.warning("Received a packet of unknown type {}. Ignoring".format(packet.packet_type))

    @staticmethod
    def _is_process():
        return multiprocessing.current_process().name != 'MainProcess'

    def __read_key(self):
        if not self.key:
            return
        # check if arg is key data
        elif re.match(r'^[0-9A-F]+$', self.key):
            return self.key
        try:
            f = open(self.key, "r")
            key = f.read().strip()
            return key
        except Exception:
            return None

    def __disconnect(self):
        to_remove = []
        for id in self._sessions.keys():
            to_remove.append(id)
        for id in to_remove:
            del self._sessions[id]

    def __on_termination_signal(self, signum, frame):
        self.__exit()

    def __exit(self):
        logger.debug('Exiting')
        for session in self._sessions.values():
            session.signal_and_close_pipes()
            session.plugin_process.join()
        if self._post_run is not None:
            self._post_run()
        sys.exit(0)

    def __on_client_connection(self, session_id, version_table):
        self._start_session_process(session_id, version_table)

    def __logs_request(self, packet):
        try:
            id_str = packet.payload.decode('utf-8')
            id = int(id_str)
        except Exception:
            logger.error('Received a broken log request from NTS: {}'.format(packet.payload))

        try:
            with open(self.__log_filename, 'r') as content_file:
                content = content_file.read()
        except Exception:
            content = ''

        response = {
            'id': id,
            'logs': content
        }

        packet = network.Packet()
        packet.set(0, network.Packet.packet_type_logs_request, 0)
        packet.write_string(json.dumps(response))

    def _autoreload(self):
        wait = 3

        if os.name == "nt":
            sub_kwargs = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP}
            break_signal = signal.CTRL_BREAK_EVENT
        else:
            sub_kwargs = {}
            break_signal = signal.SIGTERM

        # Make sure autoreload is turned off for child processes.
        sub_args = [x for x in sys.argv if x != '-r' and x != "--auto-reload"]
        popen_environ = dict(os.environ)
        popen_environ.pop('PLUGIN_AUTO_RELOAD', None)

        try:
            sub_args = [sys.executable] + sub_args
            process = subprocess.Popen(sub_args, env=popen_environ, **sub_kwargs)
        except Exception:
            logger.error("Couldn't find a suitable python executable")
            sys.exit(1)

        last_mtime = max(self.__file_times("."))
        while True:
            try:
                max_mtime = max(self.__file_times("."))
                if max_mtime > last_mtime:
                    last_mtime = max_mtime
                    logger.info("Restarting plugin")
                    process.send_signal(break_signal)
                    process = subprocess.Popen(sub_args, **sub_kwargs)
                time.sleep(wait)
            except KeyboardInterrupt:
                process.send_signal(break_signal)
                break

    def __file_times(self, path):
        found_file = False
        for root, dirs, files in os.walk(path):
            for file in filter(self.__file_filter, files):
                file_path = os.path.join(root, file)
                matched = False
                for pattern in self._to_ignore:
                    if fnmatch.fnmatch(file_path, pattern):
                        matched = True
                if matched is False:
                    found_file = True
                    yield os.stat(file_path).st_mtime
        if found_file is False:
            yield 0.0

    def __file_filter(self, name):
        return name.endswith(".py") or name.endswith(".json")

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
