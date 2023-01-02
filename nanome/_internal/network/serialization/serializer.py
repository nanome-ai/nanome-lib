from . import ContextSerialization, ContextDeserialization
from ..commands import callbacks as callbacks
from ..commands import serializers as command_serializers
from nanome._internal.network import Data
from nanome._internal.util.serializers import TypeSerializer
from nanome.util import Logs
import struct
import traceback

MESSAGE_VERSION_KEY = "ToClientProtocol"
packet_debugging = False


class Serializer(object):
    _commands = dict()
    _messages = dict()
    _command_callbacks = dict()

    def serialize_message(self, request_id, message_type, arg, version_table, expects_response):
        context = ContextSerialization(self._plugin_id, version_table, packet_debugging)
        context.write_uint(request_id)
        command_hash = callbacks.Hashes.MessageHashes[message_type]
        context.write_uint(command_hash)
        if version_table is not None:
            if version_table.get(MESSAGE_VERSION_KEY, 0) >= 1:
                context.write_bool(expects_response)

        if arg is not None:
            command = None
            try:
                command = Serializer._messages[command_hash]
            except KeyError:
                Logs.warning(
                    "Trying to serialize an unregistered message type:", message_type)
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
            command = Serializer._commands[command_hash]
        except KeyError:
            if self.try_register_session(payload) is True:
                Logs.error(
                    "A session is trying to connect even though it is already connected")
            else:
                Logs.error("Received an unregistered command:", command_hash)
            return (None, None, None)
        except BufferError as err:
            Logs.error(err)
            Logs.error(traceback.format_exc())
            return (None, None, None)
        except struct.error as err:
            Logs.error(err)
            Logs.error(traceback.format_exc())
            return (None, None, None)

        try:
            received_object = context.read_using_serializer(command)
        except BufferError as err:
            Logs.error(err)
            Logs.error(traceback.format_exc())
            return (None, None, None)
        except struct.error as err:
            Logs.error(err)
            Logs.error(traceback.format_exc())
            return (None, None, None)
        return received_object, command_hash, request_id

    def try_register_session(self, payload):
        command_hash = Data.uint_unpack(payload, 4)[0]
        return command_hash == callbacks.Hashes.CommandHashes[commands_enum.connect]

    def __init__(self):
        self._plugin_id = 0

# -------------Commands----------- #
# Commands are incoming (nanome -> plugin)


def add_command(command, serializer, callback):
    Serializer._commands[callbacks.Hashes.CommandHashes[command]] = serializer
    Serializer._command_callbacks[callbacks.Hashes.CommandHashes[command]] = callback

commands_enum = callbacks.Commands
messages_enum = callbacks.Messages
# control
add_command(
    commands_enum.connect,
    command_serializers.Connect(),
    callbacks._connect)
add_command(commands_enum.run, command_serializers.Run(), callbacks._run)
add_command(commands_enum.advanced_settings, command_serializers.AdvancedSettings(), callbacks._advanced_settings)

# workspace
add_command(commands_enum.workspace_response,
            command_serializers.ReceiveWorkspace(), callbacks._simple_callback_arg)
add_command(commands_enum.complex_add,
            command_serializers.ComplexAddedRemoved(), callbacks._complex_added)
add_command(commands_enum.complex_remove,
            command_serializers.ComplexAddedRemoved(), callbacks._complex_removed)
add_command(commands_enum.complex_list_response,
            command_serializers.ReceiveComplexList(), callbacks._simple_callback_arg)
add_command(commands_enum.complexes_response,
            command_serializers.ReceiveComplexes(), callbacks._receive_complexes)
add_command(commands_enum.structures_deep_update_done,
            command_serializers.UpdateStructuresDeepDone(), callbacks._simple_callback_no_arg)
add_command(commands_enum.add_to_workspace_done,
            command_serializers.AddToWorkspace(), callbacks._simple_callback_arg)
add_command(commands_enum.position_structures_done,
            command_serializers.PositionStructuresDone(), callbacks._simple_callback_no_arg)
add_command(commands_enum.dssp_add_done,
            command_serializers.AddDSSP(), callbacks._simple_callback_arg)
add_command(commands_enum.bonds_add_done,
            command_serializers.AddBonds(), callbacks._simple_callback_arg)
add_command(commands_enum.complex_updated,
            command_serializers.ComplexUpdated(), callbacks._complex_updated)
add_command(commands_enum.selection_changed,
            command_serializers.SelectionChanged(), callbacks._selection_changed)
add_command(commands_enum.compute_hbonds_done,
            command_serializers.ComputeHBonds(), callbacks._simple_callback_no_arg)
add_command(commands_enum.substructure_response,
            command_serializers.RequestSubstructure(), callbacks._simple_callback_arg)

# Volume
add_command(commands_enum.add_volume_done,
            command_serializers.AddVolumeDone(), callbacks._simple_callback_no_arg)

# ui
add_command(commands_enum.menu_toggle,
            command_serializers.MenuCallback(), callbacks._menu_toggled)
add_command(commands_enum.button_press,
            command_serializers.ButtonCallback(), callbacks._button_pressed)
add_command(commands_enum.button_hover,
            command_serializers.ButtonCallback(), callbacks._button_hover)
add_command(commands_enum.slider_release,
            command_serializers.SliderCallback(), callbacks._slider_released)
add_command(commands_enum.slider_change,
            command_serializers.SliderCallback(), callbacks._slider_changed)
add_command(commands_enum.text_submit,
            command_serializers.TextInputCallback(), callbacks._text_submit)
add_command(commands_enum.text_change,
            command_serializers.TextInputCallback(), callbacks._text_changed)
add_command(commands_enum.image_press,
            command_serializers.ImageCallback(), callbacks._image_pressed)
add_command(commands_enum.image_hold,
            command_serializers.ImageCallback(), callbacks._image_held)
add_command(commands_enum.image_release,
            command_serializers.ImageCallback(), callbacks._image_released)
add_command(commands_enum.dropdown_item_click,
            command_serializers.DropdownCallback(), callbacks._dropdown_item_clicked)
add_command(commands_enum.menu_transform_response,
            command_serializers.GetMenuTransformResponse(), callbacks._simple_callback_arg_unpack)

# files
add_command(commands_enum.export_files_result,
            command_serializers.ExportFiles(), callbacks._simple_callback_arg)
add_command(commands_enum.print_working_directory_response,
            command_serializers.PWD(), callbacks._simple_callback_arg_unpack)
add_command(commands_enum.cd_response,
            command_serializers.CD(), callbacks._simple_callback_arg)
add_command(commands_enum.ls_response, command_serializers.LS(
), callbacks._simple_callback_arg_unpack)
add_command(commands_enum.mv_response,
            command_serializers.MV(), callbacks._simple_callback_arg)
add_command(commands_enum.cp_response,
            command_serializers.CP(), callbacks._simple_callback_arg)
add_command(commands_enum.get_response, command_serializers.Get(
), callbacks._simple_callback_arg_unpack)
add_command(commands_enum.put_response,
            command_serializers.Put(), callbacks._simple_callback_arg)
add_command(commands_enum.rm_response,
            command_serializers.RM(), callbacks._simple_callback_arg)
add_command(commands_enum.rmdir_response,
            command_serializers.RMDir(), callbacks._simple_callback_arg)
add_command(commands_enum.mkdir_response,
            command_serializers.MKDir(), callbacks._simple_callback_arg)

# streams
add_command(commands_enum.stream_create_done,
            command_serializers.CreateStreamResult(), callbacks._receive_create_stream_result)
add_command(commands_enum.stream_feed,
            command_serializers.FeedStream(), callbacks._feed_stream)
add_command(commands_enum.stream_interrupt,
            command_serializers.InterruptStream(), callbacks._receive_interrupt_stream)
add_command(commands_enum.stream_feed_done,
            command_serializers.FeedStreamDone(), callbacks._simple_callback_no_arg)

# macros
add_command(commands_enum.get_macros_response,
            command_serializers.GetMacrosResponse(), callbacks._simple_callback_arg)
add_command(commands_enum.run_macro_result,
            command_serializers.RunMacro(), callbacks._simple_callback_arg)

# Presenter
add_command(commands_enum.presenter_info_response,
            command_serializers.GetPresenterInfoResponse(), callbacks._simple_callback_arg)
add_command(commands_enum.presenter_change,
            command_serializers.PresenterChange(), callbacks._presenter_change)
add_command(commands_enum.controller_transforms_response,
            command_serializers.GetControllerTransformsResponse(), callbacks._simple_callback_arg_unpack)

# Shape
add_command(commands_enum.set_shape_result,
            command_serializers.SetShape(), callbacks._simple_callback_arg_unpack)
add_command(commands_enum.delete_shape_result,
            command_serializers.DeleteShape(), callbacks._simple_callback_arg)

# others
add_command(commands_enum.load_file_done,
            command_serializers.LoadFileDone(), callbacks._simple_callback_arg)
add_command(commands_enum.integration,
            command_serializers.Integration(), callbacks._integration)

# -------------Messages----------- #
# Messages are outgoing (plugin -> nanome)


def add_message(command, serializer):
    Serializer._messages[callbacks.Hashes.MessageHashes[command]] = serializer

TypeSerializer.register_string_raw(MESSAGE_VERSION_KEY, 1)
# control
add_message(callbacks.Messages.connect, command_serializers.Connect())

# workspace
add_message(callbacks.Messages.workspace_update,
            command_serializers.UpdateWorkspace())
add_message(callbacks.Messages.structures_deep_update,
            command_serializers.UpdateStructures(False))
add_message(callbacks.Messages.structures_shallow_update,
            command_serializers.UpdateStructures(True))
add_message(callbacks.Messages.workspace_request,
            command_serializers.RequestWorkspace())
add_message(callbacks.Messages.complex_list_request,
            command_serializers.RequestComplexList())
add_message(callbacks.Messages.add_to_workspace,
            command_serializers.AddToWorkspace())
add_message(callbacks.Messages.complexes_request,
            command_serializers.RequestComplexes())
add_message(callbacks.Messages.bonds_add,
            command_serializers.AddBonds())
add_message(callbacks.Messages.dssp_add, command_serializers.AddDSSP())
add_message(callbacks.Messages.structures_zoom,
            command_serializers.PositionStructures())
add_message(callbacks.Messages.structures_center,
            command_serializers.PositionStructures())
add_message(callbacks.Messages.hook_complex_updated,
            command_serializers.ComplexUpdatedHook())
add_message(callbacks.Messages.hook_selection_changed,
            command_serializers.SelectionChangedHook())
add_message(callbacks.Messages.compute_hbonds,
            command_serializers.ComputeHBonds())
add_message(callbacks.Messages.substructure_request,
            command_serializers.RequestSubstructure())

# volume
add_message(callbacks.Messages.add_volume,
            command_serializers.AddVolume())

# ui
add_message(callbacks.Messages.menu_update,
            command_serializers.UpdateMenu())
add_message(callbacks.Messages.content_update,
            command_serializers.UpdateContent())
add_message(callbacks.Messages.node_update,
            command_serializers.UpdateNode())
add_message(callbacks.Messages.menu_transform_set,
            command_serializers.SetMenuTransform())
add_message(callbacks.Messages.menu_transform_request,
            command_serializers.GetMenuTransform())
add_message(callbacks.Messages.notification_send,
            command_serializers.SendNotification())
add_message(callbacks.Messages.hook_ui_callback,
            command_serializers.UIHook())

# files
add_message(callbacks.Messages.print_working_directory,
            command_serializers.PWD())
add_message(callbacks.Messages.cd, command_serializers.CD())
add_message(callbacks.Messages.ls, command_serializers.LS())
add_message(callbacks.Messages.mv, command_serializers.MV())
add_message(callbacks.Messages.cp, command_serializers.CP())
add_message(callbacks.Messages.get, command_serializers.Get())
add_message(callbacks.Messages.put, command_serializers.Put())
add_message(callbacks.Messages.rm, command_serializers.RM())
add_message(callbacks.Messages.rmdir, command_serializers.RMDir())
add_message(callbacks.Messages.mkdir, command_serializers.MKDir())

# macros
add_message(callbacks.Messages.run_macro,
            command_serializers.RunMacro())
add_message(callbacks.Messages.save_macro,
            command_serializers.SaveMacro())
add_message(callbacks.Messages.delete_macro,
            command_serializers.DeleteMacro())
add_message(callbacks.Messages.get_macros,
            command_serializers.GetMacros())
add_message(callbacks.Messages.stop_macro,
            command_serializers.StopMacro())

# streams
add_message(callbacks.Messages.stream_create,
            command_serializers.CreateStream())
add_message(callbacks.Messages.stream_feed,
            command_serializers.FeedStream())
add_message(callbacks.Messages.stream_destroy,
            command_serializers.DestroyStream())

# Presenter
add_message(callbacks.Messages.presenter_info_request,
            command_serializers.GetPresenterInfo())
add_message(callbacks.Messages.controller_transforms_request,
            command_serializers.GetControllerTransforms())

# Shape
add_message(callbacks.Messages.set_shape,
            command_serializers.SetShape())
add_message(callbacks.Messages.delete_shape,
            command_serializers.DeleteShape())

# others
add_message(callbacks.Messages.open_url, command_serializers.OpenURL())
add_message(callbacks.Messages.load_file,
            command_serializers.LoadFile())
add_message(callbacks.Messages.integration,
            command_serializers.Integration())
add_message(callbacks.Messages.set_skybox,
            command_serializers.SetSkybox())
add_message(callbacks.Messages.apply_color_scheme,
            command_serializers.ApplyColorScheme())

# files deprecated
add_message(callbacks.Messages.directory_request,
            command_serializers.DirectoryRequest())
add_message(callbacks.Messages.file_request,
            command_serializers.FileRequest())
add_message(callbacks.Messages.file_save,
            command_serializers.FileSave())
add_message(callbacks.Messages.export_files,
            command_serializers.ExportFiles())
add_message(callbacks.Messages.plugin_list_button_set,
            command_serializers.SetPluginListButton())
add_command(commands_enum.directory_response,
            command_serializers.DirectoryRequest(), callbacks._simple_callback_arg)
add_command(commands_enum.file_response,
            command_serializers.FileRequest(), callbacks._simple_callback_arg)
add_command(commands_enum.file_save_done,
            command_serializers.FileSave(), callbacks._simple_callback_arg)
