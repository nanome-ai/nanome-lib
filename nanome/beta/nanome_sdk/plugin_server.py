import asyncio
import json
import logging
import logging.config
import os
import ssl
import sys

from nanome._internal.network.packet import Packet, PacketTypes
from nanome._internal.serializer_fields import TypeSerializer
from nanome.api.serializers import CommandMessageSerializer
from nanome.beta.nanome_sdk.logs import configure_main_process_logging
from nanome.beta.nanome_sdk.utils import convert_bytes_to_packet
from nanome.beta.nanome_sdk.session import run_session_loop_py
from nanome.util.config import str2bool

__all__ = ["PluginServer"]


logger = logging.getLogger(__name__)


KEEP_ALIVE_TIME_INTERVAL = 60.0
PLUGIN_REMOTE_LOGGING = str2bool(os.environ.get('PLUGIN_REMOTE_LOGGING', False))


class PluginServer:

    def __init__(self):
        self.plugin_id = None
        self._sessions = {}
        self.plugin_class = None
        self.polling_tasks = {}

    async def run(self, nts_host, nts_port, plugin_name, description, plugin_class):
        self.plugin_class = plugin_class
        self.plugin_name = os.environ.get("PLUGIN_NAME") or plugin_name
        try:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            self.nts_reader, self.nts_writer = await asyncio.open_connection(nts_host, nts_port, ssl=ssl_context)
            self.plugin_id = await self.connect_plugin(self.plugin_name, description)
            configure_main_process_logging(self.nts_writer, self.plugin_id, self.plugin_name)
            logger.info(f"Plugin Connected. ID: {self.plugin_id}")
            self.keep_alive_task = asyncio.create_task(self.keep_alive(self.plugin_id))
            self.poll_nts_task = asyncio.create_task(self.poll_nts())
            await self.poll_nts_task
        except Exception as e:
            use_exc_info = sys.exc_info()[0] is not None
            logger.error(e, exc_info=use_exc_info)
        finally:
            self.keep_alive_task.cancel()
            self.poll_nts_task.cancel()
            self.nts_writer.close()

    async def poll_nts(self):
        """Poll NTS for packets, and forward them to the plugin server."""
        while True:
            received_bytes = await self.nts_reader.readexactly(Packet.packet_header_length)
            unpacked = Packet.header_unpack(received_bytes)
            payload_length = unpacked[4]
            received_bytes += await self.nts_reader.readexactly(payload_length)
            # logger.debug(f"Received Data from NTS. Size {len(received_bytes)}")
            await self.route_bytes(received_bytes)

    async def connect_plugin(self, name, description):
        """Send a packet to NTS to register plugin."""
        environ = os.environ
        key = environ.get("NTS_KEY", None)
        category = ""
        tags = []
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
        packet = Packet()
        plugin_id = 0
        packet.set(0, Packet.packet_type_plugin_connection, plugin_id)
        packet.write_string(json.dumps(description))
        pack = packet.pack()
        self.nts_writer.write(pack)
        await self.nts_writer.drain()
        # Wait for response containing plugin_id
        header = await self.nts_reader.readexactly(Packet.packet_header_length)
        unpacked = Packet.header_unpack(header)
        plugin_id = unpacked[3]
        return plugin_id

    async def keep_alive(self, plugin_id):
        """Long running task to send keep alive packets to NTS."""
        sleep_time = KEEP_ALIVE_TIME_INTERVAL
        while True:
            logger.debug("Sending keep alive packet.")
            packet = Packet()
            session_id = 0
            packet.payload_length = 0
            packet.session_id = session_id
            packet.plugin_id = plugin_id
            packet.packet_type = PacketTypes.keep_alive
            # packet.set(session_id, packet_type, plugin_id)
            pack = packet.pack()
            self.nts_writer.write(pack)
            await self.nts_writer.drain()
            await asyncio.sleep(sleep_time)

    async def route_bytes(self, received_bytes):
        """Route bytes from NTS to the appropriate session."""
        serializer = CommandMessageSerializer()
        packet = convert_bytes_to_packet(received_bytes)
        session_id = packet.session_id
        packet_type = packet.packet_type
        if packet_type == PacketTypes.message_to_plugin:
            # If session id does not exist, start a new session process
            if session_id not in self._sessions:
                received_version_table, _, _ = serializer.deserialize_command(packet.payload, None)
                version_table = TypeSerializer.get_best_version_table(received_version_table)
                await self.start_session_process(version_table, packet, self.plugin_class)
            else:
                process = self._sessions[session_id]
                # logger.debug(f"Writing line to session {session_id}: {len(received_bytes)} bytes")
                process.stdin.write(received_bytes)
                await process.stdin.drain()

        elif packet_type == PacketTypes.client_disconnection:
            logger.info(f"Disconnecting Session {session_id}.")
            if session_id in self._sessions:
                popen = self._sessions[session_id]
                popen.kill()
                del self._sessions[session_id]
            else:
                logger.warning(f"Session {session_id} process was already disconnected.")

        elif packet_type == PacketTypes.keep_alive:
            plugin_id = packet.plugin_id
            logger.debug(f"Keep Alive Packet received. Plugin id: {plugin_id}")
        elif packet_type == PacketTypes.plugin_list:
            logger.info("Plugin list happening?")

    async def start_session_process(self, version_table, packet, plugin_class):
        plugin_id = packet.plugin_id
        session_id = packet.session_id
        logger.info(f"Starting process for Session {session_id}")
        env = {
            **os.environ,
            'NANOME_VERSION_TABLE': json.dumps(version_table),
        }
        plugin_class_filepath = os.path.abspath(sys.modules[plugin_class.__module__].__file__)
        session_process = await asyncio.create_subprocess_exec(
            sys.executable, run_session_loop_py, str(plugin_id), str(session_id), self.plugin_name, plugin_class_filepath,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            cwd=os.getcwd(),
            env=env)
        connect_data = await session_process.stdout.readexactly(Packet.packet_header_length)
        try:
            unpacked = Packet.header_unpack(connect_data)
        except Exception:
            logger.error("Failed to unpack header")
            return
        payload_length = unpacked[4]

        connect_data += await session_process.stdout.readexactly(payload_length)
        # logger.debug(f"Writing line to NTS: {len(connect_data)} bytes")
        self.nts_writer.write(connect_data)
        self._sessions[session_id] = session_process
        self.polling_tasks[session_id] = asyncio.create_task(self.poll_session(session_process))

    async def poll_session(self, process):
        """Poll a session process for packets, and forward them to NTS."""
        while True:
            # Load header, and then payload
            try:
                outgoing_bytes = await process.stdout.readexactly(Packet.packet_header_length)
            except asyncio.IncompleteReadError:
                logger.debug("Incomplete read error. Ending session polling task.")
                break

            if not outgoing_bytes:
                logger.debug("No outgoing bytes. Ending polling task.")
                break
            _, _, _, _, payload_length = Packet.header_unpack(outgoing_bytes)
            outgoing_bytes += await process.stdout.readexactly(payload_length)

            # Pull out session logs, otherwise forward bytes to NTS
            packet = convert_bytes_to_packet(outgoing_bytes)
            if packet.packet_type == PacketTypes.live_logs:
                asyncio.create_task(self.handle_session_log_packet(packet))
            else:
                # logger.debug(f"Writing line to NTS: {len(outgoing_bytes)} bytes")
                self.nts_writer.write(outgoing_bytes)

    async def handle_session_log_packet(self, packet):
        """If the packet is a log message, use loggers in current process to handle it.

        This provides a way of rendering logs from session processes, without sending them directly to stdout.
        """
        session_logger = logging.getLogger("sessions")
        if packet.packet_type == PacketTypes.live_logs:
            # Create a log record using values from gelf dict
            gelf_dict = json.loads(packet.payload.decode("utf-8"))
            level = logging._nameToLevel[gelf_dict.get("level_name")]
            logrecord_args = {
                "name": gelf_dict.get("host"),  # or map to some other field if appropriate
                "level": level,
                "pathname": gelf_dict.get("file"),
                "lineno": gelf_dict.get("line"),
                "msg": gelf_dict.get("short_message"),
                "args": (),  # not provided in GELF
                "exc_info": None,  # not provided in GELF
            }
            logrecord = logging.LogRecord(**logrecord_args)
            logrecord.processName = gelf_dict.get("_process_name")
            session_logger.handle(logrecord)
            if PLUGIN_REMOTE_LOGGING:
                self.nts_writer.write(packet.pack())
