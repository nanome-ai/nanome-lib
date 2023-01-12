import logging
import struct
import traceback

from . import callbacks, message_serializers

from nanome._internal import enums as command_enums
from nanome._internal.network import Data
from nanome._internal.network.context import ContextSerialization, ContextDeserialization
from nanome._internal.serializer_fields import TypeSerializer
from nanome.api import files, macro, shapes, streams, structure, ui
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
    (commands_enum.menu_toggle, ui.messages.MenuCallback(), ui.callbacks.menu_toggled),
    (commands_enum.button_press, ui.messages.ButtonCallback(), ui.callbacks.button_pressed),
    (commands_enum.button_hover, ui.messages.ButtonCallback(), ui.callbacks.button_hover),
    (commands_enum.slider_release, ui.messages.SliderCallback(), ui.callbacks.slider_released),
    (commands_enum.slider_change, ui.messages.SliderCallback(), ui.callbacks.slider_changed),
    (commands_enum.text_submit, ui.messages.TextInputCallback(), ui.callbacks.text_submit),
    (commands_enum.text_change, ui.messages.TextInputCallback(), ui.callbacks.text_changed),
    (commands_enum.image_press, ui.messages.ImageCallback(), ui.callbacks.image_pressed),
    (commands_enum.image_hold, ui.messages.ImageCallback(), ui.callbacks.image_held),
    (commands_enum.image_release, ui.messages.ImageCallback(), ui.callbacks.image_released),
    (commands_enum.dropdown_item_click, ui.messages.DropdownCallback(), ui.callbacks.dropdown_item_clicked),
    (commands_enum.menu_transform_response, ui.messages.GetMenuTransformResponse(), callbacks.simple_callback_arg_unpack),
    # files
    (commands_enum.export_files_result, files.messages.ExportFiles(), callbacks.simple_callback_arg),
    (commands_enum.print_working_directory_response, files.messages.PWD(), callbacks.simple_callback_arg_unpack),
    (commands_enum.cd_response, files.messages.CD(), callbacks.simple_callback_arg),
    (commands_enum.ls_response, files.messages.LS(), callbacks.simple_callback_arg_unpack),
    (commands_enum.mv_response, files.messages.MV(), callbacks.simple_callback_arg),
    (commands_enum.cp_response, files.messages.CP(), callbacks.simple_callback_arg),
    (commands_enum.get_response, files.messages.Get(), callbacks.simple_callback_arg_unpack),
    (commands_enum.put_response, files.messages.Put(), callbacks.simple_callback_arg),
    (commands_enum.rm_response, files.messages.RM(), callbacks.simple_callback_arg),
    (commands_enum.rmdir_response, files.messages.RMDir(), callbacks.simple_callback_arg),
    (commands_enum.mkdir_response, files.messages.MKDir(), callbacks.simple_callback_arg),
    # streams
    (commands_enum.stream_create_done, streams.messages.CreateStreamResult(), callbacks.receive_create_stream_result),
    (commands_enum.stream_feed, streams.messages.FeedStream(), callbacks.feed_stream),
    (commands_enum.stream_interrupt, streams.messages.InterruptStream(), callbacks.receive_interrupt_stream),
    (commands_enum.stream_feed_done, streams.messages.FeedStreamDone(), callbacks.simple_callback_no_arg),
    # macros
    (commands_enum.get_macros_response, macro.messages.GetMacrosResponse(), callbacks.simple_callback_arg),
    (commands_enum.run_macro_result, macro.messages.RunMacro(), callbacks.simple_callback_arg),
    # Presenter
    (commands_enum.presenter_info_response, message_serializers.GetPresenterInfoResponse(), callbacks.simple_callback_arg),
    (commands_enum.presenter_change, message_serializers.PresenterChange(), callbacks.presenter_change),
    (commands_enum.controller_transforms_response, message_serializers.GetControllerTransformsResponse(), callbacks.simple_callback_arg_unpack),
    # Shape
    (commands_enum.set_shape_result, shapes.messages.SetShape(), callbacks.simple_callback_arg_unpack),
    (commands_enum.delete_shape_result, shapes.messages.DeleteShape(), callbacks.simple_callback_arg),
    # others
    (commands_enum.load_file_done, files.messages.LoadFileDone(), callbacks.simple_callback_arg),
    (commands_enum.directory_response, files.messages.DirectoryRequest(), callbacks.simple_callback_arg),
    (commands_enum.file_response, files.messages.FileRequest(), callbacks.simple_callback_arg),
    (commands_enum.file_save_done, files.messages.FileSave(), callbacks.simple_callback_arg),
    (commands_enum.integration, message_serializers.Integration(), callbacks.integration),
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
    (messages_enum.presenter_info_request, message_serializers.GetPresenterInfo()),
    (messages_enum.controller_transforms_request, message_serializers.GetControllerTransforms()),
    # Shape
    (messages_enum.set_shape, shapes.messages.SetShape()),
    (messages_enum.delete_shape, shapes.messages.DeleteShape()),
    # others
    (messages_enum.open_url, message_serializers.OpenURL()),
    (messages_enum.load_file, files.messages.LoadFile()),
    (messages_enum.integration, message_serializers.Integration()),
    (messages_enum.set_skybox, message_serializers.SetSkybox()),
    (messages_enum.apply_color_scheme, message_serializers.ApplyColorScheme()),
    # files deprecated
    (messages_enum.directory_request, files.messages.DirectoryRequest()),
    (messages_enum.file_request, files.messages.FileRequest()),
    (messages_enum.file_save, files.messages.FileSave()),
    (messages_enum.export_files, files.messages.ExportFiles()),
    (messages_enum.plugin_list_button_set, message_serializers.SetPluginListButton()),
)
