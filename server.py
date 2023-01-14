import errno
import json
import logging
import socket
import ssl
import time

from nanome._internal.network import Packet, Data, PacketTypes

from nanome._internal.serializer_fields import TypeSerializer
from nanome.api.serializers import CommandMessageSerializer


KEEP_ALIVE_TIME_INTERVAL = 60.0
KEEP_ALIVE_TIMEOUT = 15.0
PACKET_SIZE = 4096

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def send_packet(connection, packet: Packet):
    pack = packet.pack()
    total_sent = 0
    packet_len = len(pack)
    while total_sent < packet_len:
        try:
            sent = connection.send(pack)
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


def connect_to_nts(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10.0)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    connection = context.wrap_socket(sock, server_hostname="nanome.ai", suppress_ragged_eofs=False)
    try:
        logger.info(f"Connecting to server {host} {port}")
        connection.connect((host, port))
        connection.setblocking(False)
        logger.info("Connected to server")
    except (ssl.SSLError, socket.error) as e:
        connection = None
        logger.error(f"Cannot connect to server:{e}")
    return connection


def receive(received_bytes):
    # Parse received bytes into Packet instance
    data = Data()
    data.received_data(received_bytes)
    packet = Packet()
    got_header = packet.get_header(data)
    got_payload = packet.get_payload(data)
    if not got_header:
        logger.warning("Could not get packet header")
    if not got_payload:
        logger.warning("Could not get packet payload")
    return packet


def connect_plugin(connection, description):
    packet = Packet()
    plugin_id = 0
    packet.set(0, Packet.packet_type_plugin_connection, plugin_id)
    packet.write_string(json.dumps(description))
    send_packet(connection, packet)
    connect_data = None
    while not connect_data:
        try:
            connect_data = connection.recv(PACKET_SIZE)
        except ssl.SSLWantReadError:
            # time.sleep(0.01)
            continue
    current_packet = receive(connect_data)
    assert current_packet.packet_type == Packet.packet_type_plugin_connection
    return packet.plugin_id

def on_client_connection(session_id, version_table):
    logger.info(f"Session {session_id} connected!")

def route_packet(packet, connection, plugin_id, serializer):
    if packet.packet_type == Packet.packet_type_message_to_plugin:
        logger.info("Received message to plugin")
        session_id = packet.session_id
        if packet.payload:
            received_version_table, _, _ = serializer.deserialize_command(packet.payload, None)
            version_table = TypeSerializer.get_best_version_table(received_version_table)
            on_client_connection(session_id, version_table)
    elif packet.packet_type == Packet.packet_type_keep_alive:
        logger.info("Received keep alive packet")
        last_keep_alive = keep_alive(connection, last_keep_alive, plugin_id)
    elif packet.packet_type == Packet.packet_type_plugin_list:
        logger.info("Plugin list happening?")
    elif packet.packet_type == 97:
        logger.info("What does packet_type 97 mean?")


def loop_forever(connection, plugin_id):
    serializer = CommandMessageSerializer()
    while True:
        try:
            received_data = connection.recv(PACKET_SIZE)
        except ssl.SSLWantReadError:
            time.sleep(0.01)
            continue
        except ssl.SSLEOFError:
            logger.error("Connection has been forcibly closed by the server")
            break
        except KeyboardInterrupt:
            logger.warning("Server stopped by user")
            break
        else:
            packet = receive(received_data)
            try:
                packet_type = PacketTypes(packet.packet_type).name
            except ValueError:
                packet_type = packet.packet_type

            logger.debug(f"Packet received {packet_type}")
            route_packet(packet, connection, plugin_id, serializer)

def keep_alive(connection, last_keep_alive, plugin_id):
    now = time.time()
    # if waiting_keep_alive:
    #     if now - last_keep_alive >= KEEP_ALIVE_TIMEOUT:
    #         raise TimeoutError("Keep alive timeout")
    if now - last_keep_alive >= KEEP_ALIVE_TIME_INTERVAL and plugin_id >= 0:
        last_keep_alive = now
        logger.info("Sending keep alive packet")
        packet = Packet()
        packet.set(plugin_id, Packet.packet_type_keep_alive, 0)
        send_packet(connection, packet)
    return now

def get_env_data_as_dict(path: str) -> dict:
    with open(path, 'r') as f:
       return dict(tuple(line.replace('\n', '').split('=')) for line
                in f.readlines() if not line.startswith('#'))

def main():
    environ = get_env_data_as_dict('../.env.dev')
    host = environ['NTS_HOST']
    port = int(environ['NTS_PORT'])
    key = environ["NTS_KEY"]
    name = "[wip]-Server-Plugin"
    description = "This is a plugin that runs on the server"
    category = "Server"
    tags = ["server", "plugin"]
    has_advanced = False
    permissions = []
    integrations = []
    description = {
        'name': name,
        'description': description,
        'category': category,
        'tags': tags,
        'hasAdvanced': has_advanced,
        'auth': key,
        'permissions': permissions,
        'integrations': integrations
    }
    connection = connect_to_nts(host, port)
    plugin_id = connect_plugin(connection, description)
    loop_forever(connection, plugin_id)

if __name__ == "__main__":
    main()