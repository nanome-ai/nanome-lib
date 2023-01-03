from .context import ContextSerialization, ContextDeserialization
from .commands import callbacks
from .commands import serializers as command_serializers
from .commands import enums as command_enums
from nanome._internal.network import Data
from nanome._internal.util.type_serializers import TypeSerializer
import struct
import traceback
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

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
        self._register_commands(command_serializer_callback_list)
        self._register_messages(message_serializers_list)

    def serialize_message(self, request_id, message_type, arg, version_table, expects_response):
        context = ContextSerialization(
            self._plugin_id, version_table, packet_debugging)
        context.write_uint(request_id)
        command_hash = command_enums.Hashes.MessageHashes[message_type]
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
            if command.name() == "ReceiveWorkspace":
                import os
                logger.debug("Received workspace")
                with open("ReceiveWorkspaceMessage.bin", "wb") as f:
                    f.write(context._data._received_bytes)
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
        return command_hash == command_enums.Hashes.CommandHashes[commands_enum.connect]

    @classmethod
    def _register_commands(cls, command_serializer_callback_list):
        for command, serializer, callback in command_serializer_callback_list:
            cls._commands[command_enums.Hashes.CommandHashes[command]] = serializer
            cls._command_callbacks[command_enums.Hashes.CommandHashes[command]] = callback

    @classmethod
    def _register_messages(cls, command_serializer_list):
        for command, serializer in command_serializer_list:
            cls._messages[callbacks.Hashes.MessageHashes[command]] = serializer


# -------------Commands----------- #
# Commands are incoming (nanome -> plugin)commands_enum = command_enums.Commands
commands_enum = command_enums.Commands
messages_enum = command_enums.Messages
command_serializer_callback_list = (
    # control
    (commands_enum.connect, command_serializers.Connect(), callbacks.connect),
    (commands_enum.run, command_serializers.Run(), callbacks.run),
    (commands_enum.advanced_settings, command_serializers.AdvancedSettings(), callbacks.advanced_settings),
    # workspace
    (commands_enum.workspace_response, command_serializers.ReceiveWorkspace(), callbacks.simple_callback_arg),
    (commands_enum.complex_add, command_serializers.ComplexAddedRemoved(), callbacks.complex_added),
    (commands_enum.complex_remove, command_serializers.ComplexAddedRemoved(), callbacks.complex_removed),
    (commands_enum.complex_list_response, command_serializers.ReceiveComplexList(), callbacks.simple_callback_arg),
    (commands_enum.complexes_response, command_serializers.ReceiveComplexes(), callbacks.receive_complexes),
    (commands_enum.structures_deep_update_done, command_serializers.UpdateStructuresDeepDone(), callbacks.simple_callback_no_arg),
    (commands_enum.add_to_workspace_done, command_serializers.AddToWorkspace(), callbacks.simple_callback_arg),
    (commands_enum.position_structures_done, command_serializers.PositionStructuresDone(), callbacks.simple_callback_no_arg),
    (commands_enum.dssp_add_done, command_serializers.AddDSSP(), callbacks.simple_callback_arg),
    (commands_enum.bonds_add_done, command_serializers.AddBonds(), callbacks.simple_callback_arg),
    (commands_enum.complex_updated, command_serializers.ComplexUpdated(), callbacks.complex_updated),
    (commands_enum.selection_changed, command_serializers.SelectionChanged(), callbacks.selection_changed),
    (commands_enum.compute_hbonds_done, command_serializers.ComputeHBonds(), callbacks.simple_callback_no_arg),
    (commands_enum.substructure_response, command_serializers.RequestSubstructure(), callbacks.simple_callback_arg),
    # Volume
    (commands_enum.add_volume_done, command_serializers.AddVolumeDone(), callbacks.simple_callback_no_arg),
    # ui
    (commands_enum.menu_toggle, command_serializers.MenuCallback(), callbacks.menu_toggled),
    (commands_enum.button_press, command_serializers.ButtonCallback(), callbacks.button_pressed),
    (commands_enum.button_hover, command_serializers.ButtonCallback(), callbacks.button_hover),
    (commands_enum.slider_release, command_serializers.SliderCallback(), callbacks.slider_released),
    (commands_enum.slider_change, command_serializers.SliderCallback(), callbacks.slider_changed),
    (commands_enum.text_submit, command_serializers.TextInputCallback(), callbacks.text_submit),
    (commands_enum.text_change, command_serializers.TextInputCallback(), callbacks.text_changed),
    (commands_enum.image_press, command_serializers.ImageCallback(), callbacks.image_pressed),
    (commands_enum.image_hold, command_serializers.ImageCallback(), callbacks.image_held),
    (commands_enum.image_release, command_serializers.ImageCallback(), callbacks.image_released),
    (commands_enum.dropdown_item_click, command_serializers.DropdownCallback(), callbacks.dropdown_item_clicked),
    (commands_enum.menu_transform_response, command_serializers.GetMenuTransformResponse(), callbacks.simple_callback_arg_unpack),
    # files
    (commands_enum.export_files_result, command_serializers.ExportFiles(), callbacks.simple_callback_arg),
    (commands_enum.print_working_directory_response, command_serializers.PWD(), callbacks.simple_callback_arg_unpack),
    (commands_enum.cd_response, command_serializers.CD(), callbacks.simple_callback_arg),
    (commands_enum.ls_response, command_serializers.LS(), callbacks.simple_callback_arg_unpack),
    (commands_enum.mv_response, command_serializers.MV(), callbacks.simple_callback_arg),
    (commands_enum.cp_response, command_serializers.CP(), callbacks.simple_callback_arg),
    (commands_enum.get_response, command_serializers.Get(), callbacks.simple_callback_arg_unpack),
    (commands_enum.put_response, command_serializers.Put(), callbacks.simple_callback_arg),
    (commands_enum.rm_response, command_serializers.RM(), callbacks.simple_callback_arg),
    (commands_enum.rmdir_response, command_serializers.RMDir(), callbacks.simple_callback_arg),
    (commands_enum.mkdir_response, command_serializers.MKDir(), callbacks.simple_callback_arg),
    # streams
    (commands_enum.stream_create_done, command_serializers.CreateStreamResult(), callbacks.receive_create_stream_result),
    (commands_enum.stream_feed, command_serializers.FeedStream(), callbacks.feed_stream),
    (commands_enum.stream_interrupt, command_serializers.InterruptStream(), callbacks.receive_interrupt_stream),
    (commands_enum.stream_feed_done, command_serializers.FeedStreamDone(), callbacks.simple_callback_no_arg),
    # macros
    (commands_enum.get_macros_response, command_serializers.GetMacrosResponse(), callbacks.simple_callback_arg),
    (commands_enum.run_macro_result, command_serializers.RunMacro(), callbacks.simple_callback_arg),
    # Presenter
    (commands_enum.presenter_info_response, command_serializers.GetPresenterInfoResponse(), callbacks.simple_callback_arg),
    (commands_enum.presenter_change, command_serializers.PresenterChange(), callbacks.presenter_change),
    (commands_enum.controller_transforms_response, command_serializers.GetControllerTransformsResponse(), callbacks.simple_callback_arg_unpack),
    # Shape
    (commands_enum.set_shape_result, command_serializers.SetShape(), callbacks.simple_callback_arg_unpack),
    (commands_enum.delete_shape_result, command_serializers.DeleteShape(), callbacks.simple_callback_arg),

    # others
    (commands_enum.load_file_done, command_serializers.LoadFileDone(), callbacks.simple_callback_arg),
    (commands_enum.integration, command_serializers.Integration(), callbacks.integration),
    (commands_enum.directory_response, command_serializers.DirectoryRequest(), callbacks.simple_callback_arg),
    (commands_enum.file_response, command_serializers.FileRequest(), callbacks.simple_callback_arg),
    (commands_enum.file_save_done, command_serializers.FileSave(), callbacks.simple_callback_arg),
)


# -------------Messages----------- #
# Messages are outgoing (plugin -> nanome)
TypeSerializer.register_string_raw(MESSAGE_VERSION_KEY, 1)

message_serializers_list = (
    # control
    (messages_enum.connect, command_serializers.Connect()),
    # workspace
    (messages_enum.workspace_update, command_serializers.UpdateWorkspace()),
    (messages_enum.structures_deep_update, command_serializers.UpdateStructures(False)),
    (messages_enum.structures_shallow_update, command_serializers.UpdateStructures(True)),
    (messages_enum.workspace_request, command_serializers.RequestWorkspace()),
    (messages_enum.complex_list_request, command_serializers.RequestComplexList()),
    (messages_enum.add_to_workspace, command_serializers.AddToWorkspace()),
    (messages_enum.complexes_request, command_serializers.RequestComplexes()),
    (messages_enum.bonds_add, command_serializers.AddBonds()),
    (messages_enum.dssp_add, command_serializers.AddDSSP()),
    (messages_enum.structures_zoom, command_serializers.PositionStructures()),
    (messages_enum.structures_center, command_serializers.PositionStructures()),
    (messages_enum.hook_complex_updated, command_serializers.ComplexUpdatedHook()),
    (messages_enum.hook_selection_changed, command_serializers.SelectionChangedHook()),
    (messages_enum.compute_hbonds, command_serializers.ComputeHBonds()),
    (messages_enum.substructure_request, command_serializers.RequestSubstructure()),
    # volume
    (messages_enum.add_volume, command_serializers.AddVolume()),
    # ui
    (messages_enum.menu_update, command_serializers.UpdateMenu()),
    (messages_enum.content_update, command_serializers.UpdateContent()),
    (messages_enum.node_update, command_serializers.UpdateNode()),
    (messages_enum.menu_transform_set, command_serializers.SetMenuTransform()),
    (messages_enum.menu_transform_request, command_serializers.GetMenuTransform()),
    (messages_enum.notification_send, command_serializers.SendNotification()),
    (messages_enum.hook_ui_callback, command_serializers.UIHook()),
    # files
    (messages_enum.print_working_directory, command_serializers.PWD()),
    (messages_enum.cd, command_serializers.CD()),
    (messages_enum.ls, command_serializers.LS()),
    (messages_enum.mv, command_serializers.MV()),
    (messages_enum.cp, command_serializers.CP()),
    (messages_enum.get, command_serializers.Get()),
    (messages_enum.put, command_serializers.Put()),
    (messages_enum.rm, command_serializers.RM()),
    (messages_enum.rmdir, command_serializers.RMDir()),
    (messages_enum.mkdir, command_serializers.MKDir()),
    # macros
    (messages_enum.run_macro, command_serializers.RunMacro()),
    (messages_enum.save_macro, command_serializers.SaveMacro()),
    (messages_enum.delete_macro, command_serializers.DeleteMacro()),
    (messages_enum.get_macros, command_serializers.GetMacros()),
    (messages_enum.stop_macro, command_serializers.StopMacro()),
    # streams
    (messages_enum.stream_create, command_serializers.CreateStream()),
    (messages_enum.stream_feed, command_serializers.FeedStream()),
    (messages_enum.stream_destroy, command_serializers.DestroyStream()),
    # Presenter
    (messages_enum.presenter_info_request, command_serializers.GetPresenterInfo()),
    (messages_enum.controller_transforms_request, command_serializers.GetControllerTransforms()),
    # Shape
    (messages_enum.set_shape, command_serializers.SetShape()),
    (messages_enum.delete_shape, command_serializers.DeleteShape()),
    # others
    (messages_enum.open_url, command_serializers.OpenURL()),
    (messages_enum.load_file, command_serializers.LoadFile()),
    (messages_enum.integration, command_serializers.Integration()),
    (messages_enum.set_skybox, command_serializers.SetSkybox()),
    (messages_enum.apply_color_scheme, command_serializers.ApplyColorScheme()),
    # files deprecated
    (messages_enum.directory_request, command_serializers.DirectoryRequest()),
    (messages_enum.file_request, command_serializers.FileRequest()),
    (messages_enum.file_save, command_serializers.FileSave()),
    (messages_enum.export_files, command_serializers.ExportFiles()),
    (messages_enum.plugin_list_button_set, command_serializers.SetPluginListButton()),
)
