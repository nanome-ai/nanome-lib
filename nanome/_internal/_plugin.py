from . import _PluginInstance
from nanome._internal import _network as Network
from nanome._internal._process import _ProcessManager, _LogsManager
from nanome._internal._network._commands._callbacks._commands_enums import _Hashes
from nanome._internal._network._serialization._serializer import Serializer
from nanome._internal._util._serializers import _TypeSerializer
from nanome.util.logs import Logs

from multiprocessing import Process, Pipe, current_process
from timeit import default_timer as timer
import sys
import json
import cProfile
import time
import os
import fnmatch
import re
import subprocess
import signal

MAX_RECONNECT_WAIT = 20.0
KEEP_ALIVE_TIME_INTERVAL = 60.0
KEEP_ALIVE_TIMEOUT = 15.0

__metaclass__ = type


class _Plugin(object):
    __serializer = Serializer()
    _plugin_id = -1
    _custom_data = None

    def __read_key(self):
        # check if arg is key data
        if re.match(r'^[0-9A-F]+$', self.__key):
            return self.__key
        try:
            f = open(self.__key, "r")
            key = f.read().strip()
            return key
        except:
            return None

    def _on_packet_received(self, packet):
        if packet.packet_type == Network._Packet.packet_type_message_to_plugin:
            session_id = packet.session_id

            # Always look if we're trying to register a session
            #   Fix 5/27/2021 - Jeremie: We need to always check for session registration in order to fix timeout issues
            #   When NTS forces disconnection because of plugin list change, session_id still exists in self._sessions,
            #   even though it was disconnected for Nanome
            if _Plugin.__serializer.try_register_session(packet.payload) is True:
                received_version_table, _, _ = _Plugin.__serializer.deserialize_command(packet.payload, None)
                version_table = _TypeSerializer.get_best_version_table(received_version_table)
                self.__on_client_connection(session_id, version_table)
                return

            if session_id in self._sessions:
                # packet.decompress()
                self._sessions[session_id]._on_packet_received(packet.payload)
                return

            # Doesn't register? It's an error
            Logs.warning("Received a command from an unregistered session", session_id)

        elif packet.packet_type == Network._Packet.packet_type_plugin_connection:
            _Plugin._plugin_id = packet.plugin_id
            Logs.message("Registered with plugin ID", _Plugin._plugin_id, "\n=======================================\n")

        elif packet.packet_type == Network._Packet.packet_type_plugin_disconnection:
            if _Plugin._plugin_id == -1:
                if self._description['auth'] is None:
                    Logs.error("Connection refused by NTS. Are you missing a security key file?")
                else:
                    Logs.error("Connection refused by NTS. Your security key file might be invalid")
                sys.exit(1)
            else:
                Logs.message("Connection ended by NTS")
                sys.exit(0)

        elif packet.packet_type == Network._Packet.packet_type_client_disconnection:
            try:
                id = packet.session_id
                self._sessions[id].signal_and_close_pipes()
                del self._sessions[id]
                Logs.debug("Session", id, "disconnected")
            except:
                pass
        elif packet.packet_type == Network._Packet.packet_type_keep_alive:
            self.__waiting_keep_alive = False
        else:
            Logs.warning("Received a packet of unknown type", packet.packet_type, ". Ignoring")

    def __file_filter(self, name):
        return name.endswith(".py") or name.endswith(".json")

    def __file_times(self, path):
        found_file = False
        for root, dirs, files in os.walk(path):
            for file in filter(self.__file_filter, files):
                file_path = os.path.join(root, file)
                matched = False
                for pattern in self.__to_ignore:
                    if fnmatch.fnmatch(file_path, pattern):
                        matched = True
                if matched is False:
                    found_file = True
                    yield os.stat(file_path).st_mtime
        if found_file is False:
            yield 0.0

    def __autoreload(self):
        wait = 3

        if os.name == "nt":
            sub_kwargs = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP}
            break_signal = signal.CTRL_BREAK_EVENT
        else:
            sub_kwargs = {}
            break_signal = signal.SIGTERM

        sub_args = [x for x in sys.argv if x != '-r' and x != "--auto-reload"]

        try:
            sub_args = [sys.executable] + sub_args
            process = subprocess.Popen(sub_args, **sub_kwargs)
        except:
            Logs.error("Couldn't find a suitable python executable")
            sys.exit(1)

        last_mtime = max(self.__file_times("."))
        while True:
            try:
                max_mtime = max(self.__file_times("."))
                if max_mtime > last_mtime:
                    last_mtime = max_mtime
                    Logs.message("Restarting plugin")
                    process.send_signal(break_signal)
                    process = subprocess.Popen(sub_args, **sub_kwargs)
                time.sleep(wait)
            except KeyboardInterrupt:
                process.send_signal(break_signal)
                break

    def __run(self):
        if os.name == "nt":
            signal.signal(signal.SIGBREAK, self.__on_termination_signal)
        else:
            signal.signal(signal.SIGTERM, self.__on_termination_signal)
        if self._pre_run is not None:
            self._pre_run()
        _Plugin.instance = self
        self._description['auth'] = self.__read_key()
        self._process_manager = _ProcessManager()
        if self.__write_log_file:
            self._logs_manager = _LogsManager(self._plugin_class.__name__ + ".log")
        else:
            self._logs_manager = None
        self.__reconnect_attempt = 0
        self.__connect()
        self.__loop()

    def __connect(self):
        self._network = Network._NetInstance(self, _Plugin._on_packet_received)
        if self._network.connect(self.__host, self.__port):
            if _Plugin._plugin_id >= 0:
                plugin_id = _Plugin._plugin_id
            else:
                plugin_id = 0
            packet = Network._Packet()
            packet.set(0, Network._Packet.packet_type_plugin_connection, plugin_id)
            packet.write_string(json.dumps(self._description))
            self._network.send(packet)
            self.__connected = True
            self.__reconnect_attempt = 0
            self.__last_keep_alive = timer()
            for session in self._sessions.values():
                session._net_plugin = self._network
            return True
        else:
            self.__disconnection_time = timer()
            self.__reconnect_attempt += 1
            return False

    def __loop(self):
        to_remove = []
        try:
            while True:
                now = timer()

                if self.__connected is False:
                    reconnect_wait = min(2 ** self.__reconnect_attempt, MAX_RECONNECT_WAIT)
                    elapsed = now - self.__disconnection_time
                    if elapsed >= reconnect_wait:
                        Logs.message("Trying to reconnect...")
                        if self.__connect() is False:
                            if self.__reconnect_attempt == 3:
                                self.__disconnect()
                            continue
                    else:
                        time.sleep(reconnect_wait - elapsed)
                        continue
                if self._network.receive() is False:
                    self.__connected = False
                    self.__disconnection_time = timer()
                    self._network.disconnect()
                    continue

                if self.__waiting_keep_alive:
                    if now - self.__last_keep_alive >= KEEP_ALIVE_TIMEOUT:
                        self.__connected = False
                        self.__disconnection_time = timer()
                        continue
                elif now - self.__last_keep_alive >= KEEP_ALIVE_TIME_INTERVAL and _Plugin._plugin_id >= 0:
                    self.__last_keep_alive = now
                    self.__waiting_keep_alive = True
                    packet = Network._Packet()
                    packet.set(_Plugin._plugin_id, Network._Packet.packet_type_keep_alive, 0)
                    self._network.send(packet)

                del to_remove[:]
                for id, session in self._sessions.items():
                    if session._read_from_plugin() is False:
                        session.close_pipes()
                        to_remove.append(id)
                for id in to_remove:
                    self._sessions[id]._send_disconnection_message(_Plugin._plugin_id)
                    del self._sessions[id]
                self._process_manager._update()
                if self._logs_manager:
                    self._logs_manager._update()
        except KeyboardInterrupt:
            self.__exit()

    def __disconnect(self):
        to_remove = []
        for id in self._sessions.keys():
            to_remove.append(id)
        for id in to_remove:
            del self._sessions[id]

    def __on_termination_signal(self, signum, frame):
        self.__exit()

    def __exit(self):
        Logs.debug('Exiting')
        for session in _Plugin.instance._sessions.values():
            session.signal_and_close_pipes()
            session.plugin_process.join()
        if self._post_run is not None:
            self._post_run()
        sys.exit(0)

    def __on_client_connection(self, session_id, version_table):
        if session_id in self._sessions:  # If session_id already exists, close it first ()
            Logs.message("Closing session ID", session_id, "because a new session connected with the same ID")
            self._sessions[session_id].signal_and_close_pipes()
        main_conn_net, process_conn_net = Pipe()
        main_conn_proc, process_conn_proc = Pipe()
        session = Network._Session(session_id, self._network, self._process_manager, self._logs_manager, main_conn_net, main_conn_proc)
        permissions = self._description["permissions"]
        process = Process(target=_Plugin._launch_plugin, args=(self._plugin_class, session_id, process_conn_net, process_conn_proc, _Plugin.__serializer, _Plugin._plugin_id, version_table, _TypeSerializer.get_version_table(), Logs._is_verbose(), _Plugin._custom_data, permissions))
        process.start()
        session.plugin_process = process
        self._sessions[session_id] = session
        Logs.debug("Registered new session:", session_id)

    @staticmethod
    def _is_process():
        return current_process().name != 'MainProcess'

    @classmethod
    def _launch_plugin_profile(cls, plugin_class, session_id, pipe_net, pipe_proc, serializer, plugin_id, version_table, original_version_table, verbose, custom_data, permissions):
        cProfile.runctx('_Plugin._launch_plugin(plugin_class, session_id, pipe_net, pipe_proc, serializer, '
                        'plugin_id, version_table, original_version_table, verbose, custom_data,'
                        'permissions)', globals(), locals(), 'profile.out')

    @classmethod
    def _launch_plugin(cls, plugin_class, session_id, pipe_net, pipe_proc, serializer, plugin_id, version_table, original_version_table, verbose, custom_data, permissions):
        plugin = plugin_class()
        _PluginInstance.__init__(plugin, session_id, pipe_net, pipe_proc, serializer, plugin_id, version_table, original_version_table, verbose, custom_data, permissions)
        Logs.debug("Starting plugin")
        plugin._run()

    def __init__(self, name, description, tags=[], has_advanced=False, permissions=[], integrations=[]):
        self._sessions = dict()

        if isinstance(tags, str):
            tags = [tags]

        category = ""
        if len(tags) > 0:
            category = tags[0]

        for i in range(0, len(permissions)):
            permissions[i] = _Hashes.PermissionRequestHashes[permissions[i]]

        for i in range(0, len(integrations)):
            integrations[i] = _Hashes.IntegrationRequestHashes[integrations[i]]

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
        self._plugin_class = None
        self.__connected = False
        self.__has_autoreload = False
        self.__has_verbose = False
        self.__to_ignore = []
        self._pre_run = None
        self._post_run = None
        self.__waiting_keep_alive = False
