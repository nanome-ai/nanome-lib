from nanome.util import Logs
from . import _Packet

# Plugin networking representation, used from the main process
class _Session(object):
    def _read_from_plugin(self):
        try:
            has_data = self.plugin_pipe.poll()
        except:
            Logs.error("Plugin encountered an error, please check the logs")
            return False
        if has_data:
            packet = self.plugin_pipe.recv()
            self._net_plugin.send(packet)
        return True

    def _on_packet_received(self, payload):
        try:
            self.plugin_pipe.send(payload)
        except:
            Logs.error("Cannot deliver packet to plugin", self._session_id, "Did it crash?")

    def _send_disconnection_message(self, plugin_id):
        packet = _Packet()
        packet.set(self._session_id, _Packet.packet_type_plugin_disconnection, plugin_id)
        self._net_plugin.send(packet)

    def __init__(self, session_id, net_plugin):
        self._session_id = session_id
        self._net_plugin = net_plugin
        self.plugin_pipe = None
        self.plugin_process = None