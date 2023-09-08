import os
import asyncio
import inspect
import json
import logging
import logging.config
import sys
from nanome._internal.network import Packet
from nanome._internal.network.context import ContextDeserialization
from nanome.api.serializers import CommandMessageSerializer
from nanome.api import control, ui, structure
from nanome.beta.nanome_sdk.session import NanomePlugin
from nanome.beta.nanome_sdk import utils
from nanome.beta.nanome_sdk.logs import configure_session_logging

# Make sure plugin folder is in path
# Bold assumption that plugin is always in `plugin` folder
# in working directory
plugin_path = os.getcwd()  # Starting directory (/app)
sys.path.append(plugin_path)
from plugin import plugin_class  # noqa: E402


logger = logging.getLogger(__name__)


async def start_session(plugin_instance, plugin_name, plugin_id, session_id, version_table):
    if not issubclass(plugin_instance.__class__, NanomePlugin):
        logger.critical("Plugin must inherit from NanomePlugin")
        exit(1)
    plugin_instance.set_client(plugin_id, session_id, version_table)
    client = plugin_instance.client
    client.reader, client.writer = await utils.connect_stdin_stdout()
    await client.send_connect(plugin_id, session_id, version_table)
    await configure_session_logging(client.writer, plugin_id, plugin_name, session_id, plugin_instance)
    logger.info(f"Starting Session {session_id}")
    await _start_session_loop(plugin_instance)


async def _start_session_loop(plugin_instance):
    await plugin_instance.on_start()
    reader = plugin_instance.client.reader
    routing_tasks = []
    tasks = []
    while True:
        received_bytes = await reader.readexactly(Packet.packet_header_length)
        unpacked = Packet.header_unpack(received_bytes)
        payload_length = unpacked[4]
        received_bytes += await reader.readexactly(payload_length)
        packet = utils.convert_bytes_to_packet(received_bytes)
        routing_task = asyncio.create_task(_route_incoming_payload(packet.payload, plugin_instance))
        routing_tasks.append(routing_task)
        # Clear completed tasks from memory
        for i in range(len(routing_tasks) - 1, -1, -1):
            routing_task = routing_tasks[i]
            if routing_task.done():
                result = routing_task.result()
                if result and inspect.iscoroutine(result):
                    tasks.append(result)
                del routing_tasks[i]


async def _route_incoming_payload(payload, plugin_instance):
    version_table = plugin_instance.client.version_table
    context = ContextDeserialization(payload, version_table, packet_debugging=False)
    request_id = context.read_uint()
    command_hash = context.read_uint()
    message = CommandMessageSerializer._commands[command_hash]
    logger.debug(f"Session Received command: {message.name()}, Request ID {request_id}")
    if request_id in plugin_instance.client.request_futs:
        # If this is a response to a request, set the future result
        try:
            fut = plugin_instance.client.request_futs[request_id]
        except KeyError:
            logger.warning(f"Could not find future for request_id {request_id}")
            return
        else:
            fut.set_result(payload)

    # Messages that get handled by the UIManager
    ui_messages = [
        ui.messages.ButtonCallback,
        ui.messages.SliderCallback,
        ui.messages.DropdownCallback,
        ui.messages.TextInputCallback,
    ]
    # Handle Different types of messages.
    if isinstance(message, control.messages.Run):
        logger.debug("on_run_called")
        task = asyncio.create_task(plugin_instance.on_run())
        return task
    elif type(message) in ui_messages:
        logger.debug("UI Content Clicked.")
        # See if we have a registered callback for this button
        ui_manager = plugin_instance.ui_manager
        ui_command = ui_manager.find_command(command_hash)
        serializer = CommandMessageSerializer()
        received_obj_list, _, _ = serializer.deserialize_command(
            payload, version_table)
        await ui_manager.handle_ui_command(ui_command, received_obj_list)
    elif isinstance(message, structure.messages.ComplexAddedRemoved):
        logger.debug("Complex Added/Removed")
        task = asyncio.create_task(plugin_instance.on_complex_added_removed())
        return task


if __name__ == "__main__":
    plugin_id = int(sys.argv[1])
    session_id = int(sys.argv[2])
    plugin_name = sys.argv[3]
    plugin_class_filepath = sys.argv[4]

    version_table = json.loads(os.environ['NANOME_VERSION_TABLE'])
    plugin_instance = plugin_class()
    session_coro = start_session(plugin_instance, plugin_name, plugin_id, session_id, version_table)
    loop = asyncio.get_event_loop()
    session_loop = loop.run_until_complete(session_coro)
