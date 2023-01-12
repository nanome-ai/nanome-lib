import importlib
import logging
import struct
import traceback
from ..util import simple_callbacks
from ._hashes import Hashes
from nanome._internal import enums as command_enums
from nanome._internal.network import Data
from nanome._internal.network.context import ContextSerialization, ContextDeserialization
from nanome._internal.serializer_fields import TypeSerializer
from nanome.api import control, files, integration, macro, room, shapes, streams, structure, ui, user, volumetric


logger = logging.getLogger(__name__)

MESSAGE_VERSION_KEY = "ToClientProtocol"
packet_debugging = False

__all__ = ["CommandMessageSerializer", 'registered_commands', 'message_serializers_list']

# Modules which contain messages to register with the serializer
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
    command_enums = dict()
    _command_callbacks = dict()

    def __init__(self):
        self._plugin_id = 0
        Hashes.init_hashes()
        self._register_commands(registered_commands)
        self._register_messages(message_serializers_list)

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
                    f"Trying to serialize an unregistered message type: {message_type}")
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
                logger.error(f"Received an unregistered command: {command_hash}")
            return (None, None, None)
        except BufferError as err:
            logger.error(err)
            logger.error(traceback.format_exc())
            return (None, None, None)
        except struct.error as err:
            logger.error(err)
            logger.error(traceback.format_exc())
            return (None, None, None)

        try:
            logger.debug("Received command: " + command.name())
            received_object = context.read_using_serializer(command)
        except BufferError as err:
            logger.error(err)
            logger.error(traceback.format_exc())
            return (None, None, None)
        except struct.error as err:
            logger.error(err)
            logger.error(traceback.format_exc())
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


# -------------Commands----------- #
# Commands are incoming (nanome -> plugin)
Commands = command_enums.Commands

registered_commands = []
for module_str in registered_modules:
    # Get registered commands from each module
    module = importlib.import_module(module_str)
    module_commands = getattr(module, 'registered_commands', False)
    if module_commands is False:
        logger.warning('No registerd commands found in {}, Skipping'.format(module_str))
        continue
    registered_commands += module_commands


# -------------Messages----------- #
# Messages are outgoing (plugin -> nanome)
TypeSerializer.register_string_raw(MESSAGE_VERSION_KEY, 1)
messages_enum = command_enums.Messages
message_serializers_list = (
    # control
    (messages_enum.connect, control.messages.Connect()),
    (messages_enum.controller_transforms_request, control.messages.GetControllerTransforms()),
    (messages_enum.open_url, control.messages.OpenURL()),
    (messages_enum.set_skybox, room.messages.SetSkybox()),
    (messages_enum.plugin_list_button_set, control.messages.SetPluginListButton()),
    # workspace
    (messages_enum.workspace_update, structure.messages.UpdateWorkspace()),
    (messages_enum.structures_deep_update, structure.messages.UpdateStructures(False)),
    (messages_enum.structures_shallow_update, structure.messages.UpdateStructures(True)),
    (messages_enum.workspace_request, structure.messages.RequestWorkspace()),
    (messages_enum.complex_list_request, structure.messages.RequestComplexList()),
    (messages_enum.add_to_workspace, structure.messages.AddToWorkspace()),
    (messages_enum.complexes_request, structure.messages.RequestComplexes()),
    (messages_enum.bonds_add, structure.messages.AddBonds()),
    (messages_enum.dssp_add, structure.messages.AddDSSP()),
    (messages_enum.structures_zoom, structure.messages.PositionStructures()),
    (messages_enum.structures_center, structure.messages.PositionStructures()),
    (messages_enum.hook_complex_updated, structure.messages.ComplexUpdatedHook()),
    (messages_enum.hook_selection_changed, structure.messages.SelectionChangedHook()),
    (messages_enum.compute_hbonds, structure.messages.ComputeHBonds()),
    (messages_enum.substructure_request, structure.messages.RequestSubstructure()),
    (messages_enum.apply_color_scheme, structure.messages.ApplyColorScheme()),
    # volume
    (messages_enum.add_volume, volumetric.messages.AddVolume()),
    # ui
    (messages_enum.menu_update, ui.messages.UpdateMenu()),
    (messages_enum.content_update, ui.messages.UpdateContent()),
    (messages_enum.node_update, ui.messages.UpdateNode()),
    (messages_enum.menu_transform_set, ui.messages.SetMenuTransform()),
    (messages_enum.menu_transform_request, ui.messages.GetMenuTransform()),
    (messages_enum.notification_send, ui.messages.SendNotification()),
    (messages_enum.hook_ui_callback, ui.messages.UIHook()),
    # files
    (messages_enum.print_working_directory, files.messages.PWD()),
    (messages_enum.cd, files.messages.CD()),
    (messages_enum.ls, files.messages.LS()),
    (messages_enum.mv, files.messages.MV()),
    (messages_enum.cp, files.messages.CP()),
    (messages_enum.get, files.messages.Get()),
    (messages_enum.put, files.messages.Put()),
    (messages_enum.rm, files.messages.RM()),
    (messages_enum.rmdir, files.messages.RMDir()),
    (messages_enum.mkdir, files.messages.MKDir()),
    # macros
    (messages_enum.run_macro, macro.messages.RunMacro()),
    (messages_enum.save_macro, macro.messages.SaveMacro()),
    (messages_enum.delete_macro, macro.messages.DeleteMacro()),
    (messages_enum.get_macros, macro.messages.GetMacros()),
    (messages_enum.stop_macro, macro.messages.StopMacro()),
    # streams
    (messages_enum.stream_create, streams.messages.CreateStream()),
    (messages_enum.stream_feed, streams.messages.FeedStream()),
    (messages_enum.stream_destroy, streams.messages.DestroyStream()),
    # Presenter
    (messages_enum.presenter_info_request, user.messages.GetPresenterInfo()),
    # Shape
    (messages_enum.set_shape, shapes.messages.SetShape()),
    (messages_enum.delete_shape, shapes.messages.DeleteShape()),
    # others
    (messages_enum.load_file, files.messages.LoadFile()),
    # Integration
    (messages_enum.integration, integration.messages.Integration()),
    # files deprecated
    (messages_enum.directory_request, files.messages.DirectoryRequest()),
    (messages_enum.file_request, files.messages.FileRequest()),
    (messages_enum.file_save, files.messages.FileSave()),
    (messages_enum.export_files, files.messages.ExportFiles()),
)
