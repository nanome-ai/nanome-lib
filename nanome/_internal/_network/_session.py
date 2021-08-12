from nanome.util import Logs
from nanome.util.enum import IntEnum, auto
from . import _Packet
import traceback


stop_bytes = bytearray("CLOSEPIPE", "utf-8")


# Plugin networking representation, used from the main process
class _Session(object):
    def _read_from_plugin(self):
        try:
            has_net_data = self.__net_plugin_pipe.poll()
            has_proc_data = self.__proc_plugin_pipe.poll()
        except:
            Logs.error("Plugin encountered an error, please check the logs.", traceback.format_exc())
            return False
        try:
            if has_net_data:
                packet = self.__net_plugin_pipe.recv()
                if packet == stop_bytes:
                    Logs.error("Plugin encountered an error")
                    return False
                self._net_plugin.send(packet)
            if has_proc_data:
                from nanome._internal._util import _DataType
                request = self.__proc_plugin_pipe.recv()
                if request._type == _DataType.process:
                    self._process_manager._received_request(request._data, self)
                elif request._type == _DataType.log:
                    if self._logs_manager:
                        self._logs_manager._received_request(request._data)
        except EOFError:
            Logs.error("Plugin encountered an error, please check the logs.", traceback.format_exc())
            return False
        return True

    def _on_packet_received(self, payload):
        try:
            self.__net_plugin_pipe.send(payload)
        except:
            Logs.error("Cannot deliver packet to plugin", self._session_id, "Did it crash?")

    def send_process_data(self, data):
        try:
            self.__proc_plugin_pipe.send(data)
        except:
            Logs.error("Cannot deliver process info to plugin", self._session_id, "Did it crash?")

    def _send_disconnection_message(self, plugin_id):
        packet = _Packet()
        packet.set(self._session_id, _Packet.packet_type_plugin_disconnection, plugin_id)
        self._net_plugin.send(packet)

    def signal_and_close_pipes(self):
        self._on_packet_received(stop_bytes)
        self._closed = True
        self.close_pipes()

    def close_pipes(self):
        self.__net_plugin_pipe.close()
        self.__proc_plugin_pipe.close()
        self._process_manager._remove_session_processes(self._session_id)

    def __init__(self, session_id, net_plugin, process_manager, logs_manager, net_pipe, proc_pipe):
        self._session_id = session_id
        self._net_plugin = net_plugin
        self._process_manager = process_manager
        self._logs_manager = logs_manager
        self.__net_plugin_pipe = net_pipe
        self.__proc_plugin_pipe = proc_pipe
        self.plugin_process = None
        self._closed = False
