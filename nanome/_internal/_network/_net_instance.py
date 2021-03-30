from . import _Data
from . import _Packet
from nanome.util import Logs, ImportUtils

import socket
import ssl
import sys
import errno
import time
import traceback

class _NetInstance(object):
    header_state = 0
    payload_state = 1

    def __init__(self, instance, packet_callback):
        self._instance = instance
        self._on_received_packet = packet_callback
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(10.0)
        self._context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        self._context.verify_mode = ssl.CERT_NONE
        self._connection = self._context.wrap_socket(self._socket, server_hostname="nanome.ai", suppress_ragged_eofs=False)
        self._data = _Data()
        self._processing = False
        self._state = _NetInstance.header_state
        self._current_packet = _Packet()

    def connect(self, host, port):
        try:
            Logs.message("Connecting to server", host, port)
            self._connection.connect((host, port))
            self._connection.setblocking(False)
            Logs.message("Connected to server")
        except (ssl.SSLError, socket.error) as e:
            self._socket = None
            self._context = None
            self._connection = None
            Logs.error("Cannot connect to server:", e)
            return False
        return True

    def send(self, packet):
        pack = packet.pack()
        total_sent = 0
        packet_len = len(pack)
        while total_sent < packet_len:
            try:
                sent = self._connection.send(pack)
                if sent == 0:
                    return
                total_sent += sent
                pack = pack[sent:]
            except ConnectionResetError:
                Logs.error("Connection has been forcibly closed by the server")
                raise
            except ssl.SSLError:
                pass
            except socket.error as e:
                if e.errno == errno.EWOULDBLOCK or e.errno == errno.EAGAIN:
                    pass

    def disconnect(self):
        self._connection.close()

    def receive(self):
        try:
            data = self._connection.recv(4096)
        except ssl.SSLWantReadError:
            time.sleep(0.01)
        except ssl.SSLEOFError:
            Logs.error("Connection closed by plugin server")
            return False
        except KeyboardInterrupt:
            raise
        except:
            Logs.error(traceback.format_exc())
            return False
        else:
            self._received_data(data)
        return True

    def _received_data(self, data):
        self._data.received_data(data)
        self._processing = True
        while self._processing == True:
            if self._state == _NetInstance.header_state:
                if self._current_packet.get_header(self._data):
                    self._state = _NetInstance.payload_state
                else:
                    self._processing = False
            else:
                if self._current_packet.get_payload(self._data):
                    self._state = _NetInstance.header_state
                    self._on_received_packet(self._instance, self._current_packet)
                else:
                    self._processing = False
