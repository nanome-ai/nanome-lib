from nanome.util import Logs
from . import _Packet
from multiprocessing import Pipe

# Plugin networking class, used from the instance processes
class _ProcessNetwork(object):

    def _on_run(self):
        self._plugin.on_run()

    def on_advanced_settings(self):
        self._plugin.on_advanced_settings()
        
    def on_complex_added(self):
        self._plugin.on_complex_added()

    def on_complex_removed(self):
        self._plugin.on_complex_removed()

    def _call(self, request_id, *args):
        self._plugin._call(request_id, *args)

    def _close(self):
        self._process_conn.close()

    def _send(self, code, arg = None):
        command_id = self._command_id
        to_send = self._serializer.serialize_message(command_id, code, arg, self.__version_table)
        packet = _Packet()
        packet.set(self._session_id, _Packet.packet_type_message_to_client, self._plugin_id)
        packet.write(to_send)
        # if code != 0: # Messages.connect
        #     packet.compress()
        try:
            self._process_conn.send(packet)
        except (BrokenPipeError, IOError):
            pass
        self._command_id = (command_id + 1) % 4294967295 # Cap by uint max
        return command_id

    def _receive(self):
        payload = None
        try:
            has_data = self._process_conn.poll()
            if has_data:
                payload = self._process_conn.recv()
        except:
            Logs.debug("Pipe has been closed, exiting process")
            return False

        if payload:
            received_object, command_hash, request_id = self._serializer.deserialize_command(payload, self.__version_table)
            if received_object == None and command_hash == None and request_id == None:
                return True # Happens if deserialize_command returns None, an error message is already displayed in that case
                
            try:
                callback = self._serializer._command_callbacks[command_hash]
            except:
                Logs.error("Received a command without callback associated:", command_hash)
                return True
            callback(self, received_object, request_id)
        return True

    def __init__(self, plugin, session_id, pipe, serializer, plugin_id, version_table):
        self._plugin = plugin
        self._session_id = session_id
        self._process_conn = pipe
        self._serializer = serializer
        self._serializer._plugin_id = plugin_id
        self._plugin_id = plugin_id
        self._command_id = 0
        self.__version_table = version_table
