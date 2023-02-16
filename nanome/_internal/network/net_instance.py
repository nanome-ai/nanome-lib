from . import Data, Packet

import socket
import ssl
import errno
import time

import logging
logger = logging.getLogger(__name__)


class NetInstance(object):
    header_state = 0
    payload_state = 1

    def __init__(self, instance, packet_callback):
        self._instance = instance
        self._on_received_packet = packet_callback
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(10.0)
        self._context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        self._context.verify_mode = ssl.CERT_NONE
        self._connection = self._context.wrap_socket(
            self._socket, server_hostname="nanome.ai", suppress_ragged_eofs=False)
        self._data = Data()
        self._processing = False
        self._state = NetInstance.header_state
        self._current_packet = Packet()

    def connect(self, host, port):
        try:
            logger.info("Connecting to server {} {}".format(host, port))
            self._connection.connect((host, port))
            self._connection.setblocking(False)
            logger.info("Connected to server")
        except (ssl.SSLError, socket.error) as e:
            self._socket = None
            self._context = None
            self._connection = None
            logger.error("Cannot connect to server: {}".format(e))
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
            except ssl.SSLError:
                pass
            except socket.error as e:
                if e.errno == errno.EWOULDBLOCK or e.errno == errno.EAGAIN:
                    pass
            except Exception:
                # Originally caught ConnectionResetError, but not Python 2 compatible
                logger.error("Connection has been forcibly closed by the server")
                raise

    def disconnect(self):
        if self._connection is not None:
            self._connection.close()

    def receive(self):
        try:
            data = self._connection.recv(4096)
        except ssl.SSLWantReadError:
            time.sleep(0.01)
        except ssl.SSLEOFError:
            logger.error("Connection closed by plugin server")
            self._connection = None
            return False
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logger.error("Uncaught {}: {}".format(type(e).__name__, e), exc_info=1)
            time.sleep(0.1)
            self._connection = None
            return False
        else:
            if len(data) == 0:
                logger.info("Connection shutdown requested")
                return False
            self._received_data(data)
        return True

    def _received_data(self, data):
        self._data.received_data(data)
        self._processing = True

        while self._processing is True:
            if self._state == NetInstance.header_state:
                if self._current_packet.get_header(self._data):
                    self._state = NetInstance.payload_state
                else:
                    self._processing = False
            else:
                if self._current_packet.get_payload(self._data):
                    self._state = NetInstance.header_state
                    self._on_received_packet(self._instance, self._current_packet)
                else:
                    self._processing = False
