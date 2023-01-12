import logging
import struct
import traceback

from . import callbacks, message_serializers

from nanome._internal import enums as command_enums
from nanome._internal.network import Data
from nanome._internal.network.context import ContextSerialization, ContextDeserialization
from nanome._internal.serializer_fields import TypeSerializer
from nanome.api import structure
from ._hashes import Hashes


logger = logging.getLogger(__name__)

MESSAGE_VERSION_KEY = "ToClientProtocol"
packet_debugging = False

__all__ = ["CommandMessageSerializer", 'command_serializer_callback_list', 'message_serializers_list']


class CommandMessageSerializer(object):
    _commands = dict()
    _messages = dict()
    command_enums = dict()
    _command_callbacks = dict()

    def __init__(self):
        self._plugin_id = 0
        Hashes.init_hashes()
        self._register_commands(command_serializer_callback_list)
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
        return command_hash == Hashes.CommandHashes[commands_enum.connect]

    @classmethod
    def _register_commands(cls, command_serializer_callback_list):
        for command, serializer, callback in command_serializer_callback_list:
            cls._commands[Hashes.CommandHashes[command]] = serializer
            cls._command_callbacks[Hashes.CommandHashes[command]] = callback

    @classmethod
    def _register_messages(cls, command_serializer_list):
        for command, serializer in command_serializer_list:
            cls._messages[callbacks.Hashes.MessageHashes[command]] = serializer


# -------------Commands----------- #
# Commands are incoming (nanome -> plugin)
commands_enum = command_enums.Commands
command_serializer_callback_list = (
    # control
    (commands_enum.connect, message_serializers.Connect(), callbacks.connect),
    (commands_enum.run, message_serializers.Run(), callbacks.run),
    (commands_enum.advanced_settings, message_serializers.AdvancedSettings(), callbacks.advanced_settings),
    # workspace
    (commands_enum.workspace_response, structure.messages.ReceiveWorkspace(), callbacks.simple_callback_arg),
    (commands_enum.complex_add, structure.messages.ComplexAddedRemoved(), structure.callbacks.complex_added),
    (commands_enum.complex_remove, structure.messages.ComplexAddedRemoved(), structure.callbacks.complex_removed),
    (commands_enum.complex_list_response, structure.messages.ReceiveComplexList(), callbacks.simple_callback_arg),
    (commands_enum.complexes_response, structure.messages.ReceiveComplexes(), structure.callbacks.receive_complexes),
    (commands_enum.structures_deep_update_done, structure.messages.UpdateStructuresDeepDone(), callbacks.simple_callback_no_arg),
    (commands_enum.add_to_workspace_done, structure.messages.AddToWorkspace(), callbacks.simple_callback_arg),
    (commands_enum.position_structures_done, structure.messages.PositionStructuresDone(), callbacks.simple_callback_no_arg),
    (commands_enum.dssp_add_done, structure.messages.AddDSSP(), callbacks.simple_callback_arg),
    (commands_enum.bonds_add_done, structure.messages.AddBonds(), callbacks.simple_callback_arg),
    (commands_enum.complex_updated, structure.messages.ComplexUpdated(), structure.callbacks.complex_updated),
    (commands_enum.selection_changed, structure.messages.SelectionChanged(), structure.callbacks.selection_changed),
    (commands_enum.compute_hbonds_done, structure.messages.ComputeHBonds(), callbacks.simple_callback_no_arg),
    (commands_enum.substructure_response, structure.messages.RequestSubstructure(), callbacks.simple_callback_arg),
    # Volume
    (commands_enum.add_volume_done, message_serializers.AddVolumeDone(), callbacks.simple_callback_no_arg),
    # ui
    (commands_enum.menu_toggle, message_serializers.MenuCallback(), callbacks.menu_toggled),
    (commands_enum.button_press, message_serializers.ButtonCallback(), callbacks.button_pressed),
    (commands_enum.button_hover, message_serializers.ButtonCallback(), callbacks.button_hover),
    (commands_enum.slider_release, message_serializers.SliderCallback(), callbacks.slider_released),
    (commands_enum.slider_change, message_serializers.SliderCallback(), callbacks.slider_changed),
    (commands_enum.text_submit, message_serializers.TextInputCallback(), callbacks.text_submit),
    (commands_enum.text_change, message_serializers.TextInputCallback(), callbacks.text_changed),
    (commands_enum.image_press, message_serializers.ImageCallback(), callbacks.image_pressed),
    (commands_enum.image_hold, message_serializers.ImageCallback(), callbacks.image_held),
    (commands_enum.image_release, message_serializers.ImageCallback(), callbacks.image_released),
    (commands_enum.dropdown_item_click, message_serializers.DropdownCallback(), callbacks.dropdown_item_clicked),
    (commands_enum.menu_transform_response, message_serializers.GetMenuTransformResponse(), callbacks.simple_callback_arg_unpack),
    # files
    (commands_enum.export_files_result, message_serializers.ExportFiles(), callbacks.simple_callback_arg),
    (commands_enum.print_working_directory_response, message_serializers.PWD(), callbacks.simple_callback_arg_unpack),
    (commands_enum.cd_response, message_serializers.CD(), callbacks.simple_callback_arg),
    (commands_enum.ls_response, message_serializers.LS(), callbacks.simple_callback_arg_unpack),
    (commands_enum.mv_response, message_serializers.MV(), callbacks.simple_callback_arg),
    (commands_enum.cp_response, message_serializers.CP(), callbacks.simple_callback_arg),
    (commands_enum.get_response, message_serializers.Get(), callbacks.simple_callback_arg_unpack),
    (commands_enum.put_response, message_serializers.Put(), callbacks.simple_callback_arg),
    (commands_enum.rm_response, message_serializers.RM(), callbacks.simple_callback_arg),
    (commands_enum.rmdir_response, message_serializers.RMDir(), callbacks.simple_callback_arg),
    (commands_enum.mkdir_response, message_serializers.MKDir(), callbacks.simple_callback_arg),
    # streams
    (commands_enum.stream_create_done, message_serializers.CreateStreamResult(), callbacks.receive_create_stream_result),
    (commands_enum.stream_feed, message_serializers.FeedStream(), callbacks.feed_stream),
    (commands_enum.stream_interrupt, message_serializers.InterruptStream(), callbacks.receive_interrupt_stream),
    (commands_enum.stream_feed_done, message_serializers.FeedStreamDone(), callbacks.simple_callback_no_arg),
    # macros
    (commands_enum.get_macros_response, message_serializers.GetMacrosResponse(), callbacks.simple_callback_arg),
    (commands_enum.run_macro_result, message_serializers.RunMacro(), callbacks.simple_callback_arg),
    # Presenter
    (commands_enum.presenter_info_response, message_serializers.GetPresenterInfoResponse(), callbacks.simple_callback_arg),
    (commands_enum.presenter_change, message_serializers.PresenterChange(), callbacks.presenter_change),
    (commands_enum.controller_transforms_response, message_serializers.GetControllerTransformsResponse(), callbacks.simple_callback_arg_unpack),
    # Shape
    (commands_enum.set_shape_result, message_serializers.SetShape(), callbacks.simple_callback_arg_unpack),
    (commands_enum.delete_shape_result, message_serializers.DeleteShape(), callbacks.simple_callback_arg),
    # others
    (commands_enum.load_file_done, message_serializers.LoadFileDone(), callbacks.simple_callback_arg),
    (commands_enum.integration, message_serializers.Integration(), callbacks.integration),
    (commands_enum.directory_response, message_serializers.DirectoryRequest(), callbacks.simple_callback_arg),
    (commands_enum.file_response, message_serializers.FileRequest(), callbacks.simple_callback_arg),
    (commands_enum.file_save_done, message_serializers.FileSave(), callbacks.simple_callback_arg),
)


# -------------Messages----------- #
# Messages are outgoing (plugin -> nanome)
TypeSerializer.register_string_raw(MESSAGE_VERSION_KEY, 1)
messages_enum = command_enums.Messages
message_serializers_list = (
    # control
    (messages_enum.connect, message_serializers.Connect()),
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
    # volume
    (messages_enum.add_volume, message_serializers.AddVolume()),
    # ui
    (messages_enum.menu_update, message_serializers.UpdateMenu()),
    (messages_enum.content_update, message_serializers.UpdateContent()),
    (messages_enum.node_update, message_serializers.UpdateNode()),
    (messages_enum.menu_transform_set, message_serializers.SetMenuTransform()),
    (messages_enum.menu_transform_request, message_serializers.GetMenuTransform()),
    (messages_enum.notification_send, message_serializers.SendNotification()),
    (messages_enum.hook_ui_callback, message_serializers.UIHook()),
    # files
    (messages_enum.print_working_directory, message_serializers.PWD()),
    (messages_enum.cd, message_serializers.CD()),
    (messages_enum.ls, message_serializers.LS()),
    (messages_enum.mv, message_serializers.MV()),
    (messages_enum.cp, message_serializers.CP()),
    (messages_enum.get, message_serializers.Get()),
    (messages_enum.put, message_serializers.Put()),
    (messages_enum.rm, message_serializers.RM()),
    (messages_enum.rmdir, message_serializers.RMDir()),
    (messages_enum.mkdir, message_serializers.MKDir()),
    # macros
    (messages_enum.run_macro, message_serializers.RunMacro()),
    (messages_enum.save_macro, message_serializers.SaveMacro()),
    (messages_enum.delete_macro, message_serializers.DeleteMacro()),
    (messages_enum.get_macros, message_serializers.GetMacros()),
    (messages_enum.stop_macro, message_serializers.StopMacro()),
    # streams
    (messages_enum.stream_create, message_serializers.CreateStream()),
    (messages_enum.stream_feed, message_serializers.FeedStream()),
    (messages_enum.stream_destroy, message_serializers.DestroyStream()),
    # Presenter
    (messages_enum.presenter_info_request, message_serializers.GetPresenterInfo()),
    (messages_enum.controller_transforms_request, message_serializers.GetControllerTransforms()),
    # Shape
    (messages_enum.set_shape, message_serializers.SetShape()),
    (messages_enum.delete_shape, message_serializers.DeleteShape()),
    # others
    (messages_enum.open_url, message_serializers.OpenURL()),
    (messages_enum.load_file, message_serializers.LoadFile()),
    (messages_enum.integration, message_serializers.Integration()),
    (messages_enum.set_skybox, message_serializers.SetSkybox()),
    (messages_enum.apply_color_scheme, message_serializers.ApplyColorScheme()),
    # files deprecated
    (messages_enum.directory_request, message_serializers.DirectoryRequest()),
    (messages_enum.file_request, message_serializers.FileRequest()),
    (messages_enum.file_save, message_serializers.FileSave()),
    (messages_enum.export_files, message_serializers.ExportFiles()),
    (messages_enum.plugin_list_button_set, message_serializers.SetPluginListButton()),
)
