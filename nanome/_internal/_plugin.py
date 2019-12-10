from . import _PluginInstance
from nanome._internal import _network as Network
from nanome._internal._process import _ProcessManager
from nanome._internal._network._serialization._serializer import Serializer
from nanome._internal._util._serializers import _TypeSerializer
from nanome.util.logs import Logs
from nanome.util import config

from multiprocessing import Process, Pipe, current_process
from timeit import default_timer as timer
import sys
import json
import cProfile
import time
import os

try_reconnection_time = 20.0
keep_alive_time_interval = 3600.0

__metaclass__ = type
class _Plugin(object):
    __serializer = Serializer()
    _plugin_id = -1
    _custom_data = None

    def __parse_args(self):
        Logs._set_verbose(False)
        for i in range(1, len(sys.argv)):
            if sys.argv[i] == "-h":
                Logs.message("Usage:", sys.argv[1],"[-h] [-a ADDRESS] [-p PORT]")
                Logs.message(" -h                   display this help")
                Logs.message(" -a                   connects to a NTS at the specified IP address")
                Logs.message(" -p                   connects to a NTS at the specified port")
                Logs.message(" -k                   specifies a key file to use to connect to NTS")
                Logs.message(" -n                   name to display for this plugin in Nanome")
                Logs.message(" -v                   enable verbose mode, to display Logs.debug")
                Logs.message(" -r, --auto-reload    restart plugin automatically if a python file in current directory changes")
                sys.exit(0)
            elif sys.argv[i] == "-a":
                if i >= len(sys.argv):
                    Logs.error("Error: -a requires an argument")
                    sys.exit(1)
                self.__host = sys.argv[i + 1]
                i += 1
            elif sys.argv[i] == "-p":
                if i >= len(sys.argv):
                    Logs.error("Error: -p requires an argument")
                    sys.exit(1)
                try:
                    self.__port = int(sys.argv[i + 1])
                except ValueError:
                    Logs.error("Error: -p argument has to be an integer")
                    sys.exit(1)
                i += 1
            elif sys.argv[i] == "-k":
                if i >= len(sys.argv):
                    Logs.error("Error: -k requires an argument")
                    sys.exit(1)
                self.__key_file = sys.argv[i + 1]
                i += 1
            elif sys.argv[i] == "-n":
                if i >= len(sys.argv):
                    Logs.error("Error: -n requires an argument")
                    sys.exit(1)
                self._description['name'] = sys.argv[i + 1]
                i += 1
            elif sys.argv[i] == "-v":
                Logs._set_verbose(True)
            elif sys.argv[i] == "-r" or sys.argv[i] == "--auto-reload":
                self.__has_autoreload = True

    def __read_key_file(self):
        try:
            f = open(self.__key_file, "r")
            key = f.read()
            return key
        except:
            return None

    def _on_packet_received(self, packet):
        if packet.packet_type == Network._Packet.packet_type_message_to_plugin:
            session_id = packet.session_id
            if session_id in self._sessions:
                # packet.decompress()
                self._sessions[session_id]._on_packet_received(packet.payload)
                return

            # If we don't know this session_id, try to register it first
            if _Plugin.__serializer.try_register_session(packet.payload) == True:
                received_version_table, _, _ = _Plugin.__serializer.deserialize_command(packet.payload, None)
                version_table = _TypeSerializer.get_best_version_table(received_version_table)
                self.__on_client_connection(session_id, version_table)

            # Doesn't register? It's an error
            else:
                Logs.warning("Received a command from an unregistered session", session_id)

        elif packet.packet_type == Network._Packet.packet_type_plugin_connection:
            _Plugin._plugin_id = packet.plugin_id
            Logs.message("Registered with plugin ID", _Plugin._plugin_id, "\n=======================================\n")

        elif packet.packet_type == Network._Packet.packet_type_plugin_disconnection:
            if _Plugin._plugin_id == -1:
                if self._description['auth'] == None:
                    Logs.error("Connection refused by NTS. Are you missing a security key file?")
                else:
                    Logs.error("Connection refused by NTS. Your security key file might be invalid")
                sys.exit(1)
            else:
                Logs.debug("Connection ended by NTS")
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
            pass
        else:
            Logs.warning("Received a packet of unknown type", packet.packet_type, ". Ignoring")

    def __file_filter(self, name):
        return name.endswith(".py")

    def __file_times(self, path):
        for top_level in filter(self.__file_filter, os.listdir(".")):
            for root, dirs, files in os.walk(top_level):
                for file in filter(self.__file_filter, files):
                    yield os.stat(os.path.join(root, file)).st_mtime

    def __autoreload(self):
        # def print_stdout(process):
        #     stdout = process.stdout
        #     if stdout != None:
        #         print stdout

        # How often we check the filesystem for changes (in seconds)
        wait = 1

        # The process to autoreload
        process = Process(target=_Plugin._run_autoreload, args=(self,))
        process.start()

        # The current maximum file modified time under the watched directory
        last_mtime = max(self.__file_times("."))
        while True:
            max_mtime = max(self.__file_times("."))
            # print_stdout(process)
            if max_mtime > last_mtime:
                last_mtime = max_mtime
                Logs.debug("Restarting plugin")
                process.kill()
                process = Process(target=_Plugin._run_autoreload, args=(self,))
                process.start()
            time.sleep(wait)

    @classmethod
    def _run_autoreload(cls, self):
        self.__run()

    def __run(self):
        _Plugin.instance = self
        self._description['auth'] = self.__read_key_file()
        self._process_manager = _ProcessManager()
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
            self.__last_keep_alive = timer()
            return True
        else:
            self.__disconnection_time = timer()
            return False

    def __loop(self):
        to_remove = []
        try:
            while True:
                if self.__connected == False:
                    elapsed = timer() - self.__disconnection_time
                    if elapsed >= try_reconnection_time:
                        Logs.message("Trying to reconnect...")
                        if self.__connect() == False:
                            self.__disconnection_time = timer()
                            continue
                    else:
                        time.sleep(try_reconnection_time - elapsed)
                        continue
                if self._network.receive() == False:
                    self.__connected = False
                    self.__disconnect()
                    continue
                if timer() - self.__last_keep_alive >= keep_alive_time_interval:
                    self.__last_keep_alive = timer()
                    packet = Network._Packet()
                    packet.set(_Plugin._plugin_id, Network._Packet.packet_type_keep_alive, 0)
                    self._network.send(packet)
                to_remove.clear()
                for id, session in self._sessions.items():
                    if session._read_from_plugin() == False:
                        session.close_pipes()
                        to_remove.append(id)
                for id in to_remove:
                    self._sessions[id]._send_disconnection_message(_Plugin._plugin_id)
                    del self._sessions[id]
                self._process_manager._update()
        except KeyboardInterrupt:
            self.__exit()

    def __disconnect(self):
        to_remove = []
        for id in self._sessions.keys():
            to_remove.append(id)
        for id in to_remove:
            del self._sessions[id]
        self.__disconnection_time = timer()

    def __exit(self):
        Logs.debug('Exiting')
        for session in _Plugin.instance._sessions.values():
            session.signal_and_close_pipes()
            session.plugin_process.join()
        sys.exit(0)

    def __on_client_connection(self, session_id, version_table):
        main_conn_net, process_conn_net = Pipe()
        main_conn_proc, process_conn_proc = Pipe()
        session = Network._Session(session_id, self._network, self._process_manager, main_conn_net, main_conn_proc)
        process = Process(target=_Plugin._launch_plugin, args=(self._plugin_class, session_id, process_conn_net, process_conn_proc, _Plugin.__serializer, _Plugin._plugin_id, version_table, _TypeSerializer.get_version_table(), Logs._is_verbose(), _Plugin._custom_data))
        process.start()
        session.plugin_process = process
        self._sessions[session_id] = session
        Logs.debug("Registered new session:", session_id)

    @staticmethod
    def _is_process():
        return current_process().name != 'MainProcess'

    @classmethod
    def _launch_plugin_profile(cls, plugin_class, session_id, pipe_net, pipe_proc, serializer, plugin_id, version_table, original_version_table, verbose, custom_data):
        cProfile.runctx('_Plugin._launch_plugin(plugin_class, session_id, pipe_net, pipe_proc, serializer, plugin_id, version_table, original_version_table, verbose, custom_data)', globals(), locals(), 'profile.out')

    @classmethod
    def _launch_plugin(cls, plugin_class, session_id, pipe_net, pipe_proc, serializer, plugin_id, version_table, original_version_table, verbose, custom_data):
        plugin = plugin_class()
        _PluginInstance.__init__(plugin, session_id, pipe_net, pipe_proc, serializer, plugin_id, version_table, original_version_table, verbose, custom_data)
        Logs.debug("Starting plugin")
        plugin._run()

    def __init__(self, name, description, category = "", has_advanced = False):
        self._sessions = dict()
        self._description = {
            'name': name,
            'description': description,
            'category': category,
            'hasAdvanced': has_advanced,
            'auth': None
        }
        self._plugin_class = None
        self.__connected = False
        self.__has_autoreload = False
