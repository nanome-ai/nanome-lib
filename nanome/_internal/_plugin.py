from . import _PluginInstance
from nanome._internal import _network as Network
from nanome._internal._network._serialization._serializer import Serializer
from nanome._internal._util._serializers import _TypeSerializer
from nanome.util.logs import Logs

from multiprocessing import Process, Pipe, current_process
import sys
import json
import cProfile

__metaclass__ = type
class _Plugin(object):
    __serializer = Serializer()
    _plugin_id = -1

    def __parse_args(self):
        Logs.set_verbose(False)
        for i in range(1, len(sys.argv)):
            if sys.argv[i] == "-h":
                Logs.message("Usage:", sys.argv[1],"[-h] [-a ADDRESS] [-p PORT]")
                Logs.message(" -h  display this help")
                Logs.message(" -a  connects to a NTS at the specified IP address")
                Logs.message(" -p  connects to a NTS at the specified port")
                Logs.message(" -k  specifies a key file to use to connect to NTS")
                Logs.message(" -v  enable verbose mode, to display Logs.debug")
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
            elif sys.argv[i] == "-v":
                Logs.set_verbose(True)

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
                self._sessions[id].plugin_pipe.close()
                del self._sessions[id]
                Logs.debug("Session", id, "disconnected")
            except:
                pass
        else:
            Logs.warning("Received a packet of unknown type", packet.packet_type, ". Ignoring")

    def __run(self):
        _Plugin.instance = self
        self._description['auth'] = self.__read_key_file()
        self._network = Network._NetInstance(self, _Plugin._on_packet_received)
        self._network.connect(self.__host, self.__port)
        packet = Network._Packet()
        packet.set(0, Network._Packet.packet_type_plugin_connection, 0)
        packet.write_string(json.dumps(self._description))
        self._network.send(packet)
        self.__loop()

    def __loop(self):
        try:
            while True:
                to_remove = []
                if self._network.receive() == False:
                    self.__exit()
                for id, session in self._sessions.items():
                    if session._read_from_plugin() == False:
                        to_remove.append(id)
                for id in to_remove:
                    self._sessions[id]._send_disconnection_message(_Plugin._plugin_id)
                    del self._sessions[id]
        except KeyboardInterrupt:
            self.__exit()

    def __exit(self):
        Logs.debug('Exiting')
        for session in _Plugin.instance._sessions.values():
            session.plugin_pipe.close()
            session.plugin_process.join()
        sys.exit(0)

    def __on_client_connection(self, session_id, version_table):
        session = Network._Session(session_id, self._network)
        main_conn, process_conn = Pipe()
        session.plugin_pipe = main_conn
        process = Process(target=_Plugin._launch_plugin, args=(self._plugin_class, session_id, process_conn, _Plugin.__serializer, _Plugin._plugin_id, version_table, _TypeSerializer.get_version_table(), Logs.is_verbose()))
        process.start()
        session.plugin_process = process
        self._sessions[session_id] = session
        Logs.debug("Registered new session:", session_id)

    @staticmethod
    def _is_process():
        return current_process().name != 'MainProcess'

    @classmethod
    def _launch_plugin_profile(cls, plugin_class, session_id, pipe, serializer, plugin_id, version_table, original_version_table, verbose):
        cProfile.runctx('_Plugin._launch_plugin(plugin_class, session_id, pipe, serializer, plugin_id, version_table, original_version_table, verbose)', globals(), locals(), 'profile.out')

    @classmethod
    def _launch_plugin(cls, plugin_class, session_id, pipe, serializer, plugin_id, version_table, original_version_table, verbose):
        plugin = plugin_class()
        _PluginInstance.__init__(plugin, session_id, pipe, serializer, plugin_id, version_table, original_version_table, verbose)
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