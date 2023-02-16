import importlib
import logging
import struct
from ._hashes import Hashes
from nanome._internal.enums import Commands
from nanome._internal.network import Data
from nanome._internal.network.context import ContextSerialization, ContextDeserialization


logger = logging.getLogger(__name__)

MESSAGE_VERSION_KEY = "ToClientProtocol"
packet_debugging = False

__all__ = ["CommandMessageSerializer", 'registered_commands', 'registered_messages']

# Modules which contain commands and messages to register with the serializer
registered_modules = [
    'nanome.api.control',
    'nanome.api.files',
    'nanome.api.integration',
    'nanome.api.macro',
    'nanome.api.room',
    'nanome.api.shapes',
    'nanome.api.streams',
    'nanome.api.structure',
    'nanome.api.ui',
    'nanome.api.user',
    'nanome.api.volumetric',
]


class CommandMessageSerializer(object):
    _commands = dict()
    _messages = dict()
    _command_callbacks = dict()

    def __init__(self):
        self._plugin_id = 0
        Hashes.init_hashes()
        self._register_commands(registered_commands)
        self._register_messages(registered_messages)

    def serialize_message(self, request_id, message_type, arg, version_table, expects_response):
        context = ContextSerialization(self._plugin_id, version_table, packet_debugging)
        context.write_uint(request_id)
        command_hash = Hashes.MessageHashes[message_type]
        context.write_uint(command_hash)
        if version_table is not None:
            if version_table.get(MESSAGE_VERSION_KEY, 0) >= 1:
                context.write_bool(expects_response)

        if arg is not None:
            command = None
            try:
                command = CommandMessageSerializer._messages[command_hash]
            except KeyError:
                logger.warning(
                    "Trying to serialize an unregistered message type: {}".format(message_type)
                )
            if command is not None:
                context.write_using_serializer(command, arg)
                return context.to_array()
        return context.to_array()

    def deserialize_command(self, payload, version_table):
        context = ContextDeserialization(
            payload, version_table, packet_debugging)
        try:
            request_id = context.read_uint()
            command_hash = context.read_uint()
            command = CommandMessageSerializer._commands[command_hash]
        except KeyError:
            if self.try_register_session(payload) is True:
                logger.error("A session is trying to connect even though it is already connected")
            else:
                logger.error("Received an unregistered command: {}".format(command_hash))
            return (None, None, None)
        except (BufferError, struct.error) as err:
            logger.error(err, exc_info=1)
            return (None, None, None)

        try:
            logger.debug("Received command: " + command.name())
            received_object = context.read_using_serializer(command)
        except (BufferError, struct.error) as err:
            logger.error(err, exc_info=1)
            return (None, None, None)

        return received_object, command_hash, request_id

    def try_register_session(self, payload):
        command_hash = Data.uint_unpack(payload, 4)[0]
        return command_hash == Hashes.CommandHashes[Commands.connect]

    @classmethod
    def _register_commands(cls, registered_commands):
        for command, serializer, callback in registered_commands:
            cls._commands[Hashes.CommandHashes[command]] = serializer
            cls._command_callbacks[Hashes.CommandHashes[command]] = callback

    @classmethod
    def _register_messages(cls, command_serializer_list):
        for command, serializer in command_serializer_list:
            cls._messages[Hashes.MessageHashes[command]] = serializer


"""
Register commands and messages with the serializer

Messages are outgoing (plugin -> nanome)
Commands are incoming (nanome -> plugin)
"""

registered_commands = []
registered_messages = []
for module_str in registered_modules:
    # Get registered commands from each module
    module = importlib.import_module(module_str)
    module_commands = getattr(module, 'registered_commands', False)
    module_messages = getattr(module, 'registered_messages', False)
    if module_commands is False and module_messages is False:
        logger.warning('No registered commands or messages found in {}, Skipping'.format(module_str))
        continue
    if module_commands:
        registered_commands += module_commands
    if module_messages:
        registered_messages += module_messages
