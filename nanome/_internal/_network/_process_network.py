from nanome.util import Logs
from nanome._internal._util._serializers import _CachedImageSerializer
from . import _Packet

stop_bytes = bytearray("CLOSEPIPE", "utf-8")

# Plugin networking class, used from the instance processes


class _ProcessNetwork(object):

    _instance = None

    def _on_run(self):
        self._plugin.on_run()

    def on_advanced_settings(self):
        self._plugin.on_advanced_settings()

    def on_complex_added(self):
        self._plugin.on_complex_added()

    def on_complex_removed(self):
        self._plugin.on_complex_removed()

    def _on_presenter_change(self):
        self._plugin.on_presenter_change()

    def _call(self, request_id, *args):
        self._plugin._call(request_id, *args)

    def _close(self):
        self._process_conn.send(stop_bytes)
        self._process_conn.close()

    @classmethod
    def _send_connect(cls, code, arg):
        return cls.__send(code, None, arg, False)

    @classmethod
    def _send(cls, code, arg, expects_response):
        return cls.__send(code, cls._instance.__version_table, arg, expects_response)

    @classmethod
    def __send(cls, code, version_table, arg, expects_response):
        self = cls._instance
        command_id = self._command_id
        to_send = self._serializer.serialize_message(command_id, code, arg, version_table, expects_response)
        packet = _Packet()
        packet.set(self._session_id, _Packet.packet_type_message_to_client, self._plugin_id)
        packet.write(to_send)
        # if code != 0: # Messages.connect
        #     packet.compress()
        try:
            self._process_conn.send(packet)
        except BrokenPipeError:
            pass  # Ignore, as it will be closed later on, during _receive
        self._command_id = (command_id + 1) % 4294967295  # Cap by uint max
        return command_id

    def _receive(self):
        payload = None
        try:
            has_data = self._process_conn.poll()
            if has_data:
                payload = self._process_conn.recv()
        except BrokenPipeError:
            Logs.debug("Pipe has been closed, exiting process")
            self._plugin._on_stop()
            return False

        if payload:
            if payload == stop_bytes:
                Logs.debug("Pipe has been closed, exiting process")
                self._plugin._on_stop()
                return False

            received_object, command_hash, request_id = self._serializer.deserialize_command(payload, self.__version_table)
            if received_object == None and command_hash == None and request_id == None:
                return True  # Happens if deserialize_command returns None, an error message is already displayed in that case

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

        _CachedImageSerializer.session = session_id

        _ProcessNetwork._instance = self
