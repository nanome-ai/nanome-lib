from . import ContextSerialization, ContextDeserialization
from ..commands import callbacks as CommandCallbacks
from ..commands import serializers as CommandSerializers
from nanome._internal.network import Data
from nanome._internal.util import serializers as Serializers
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
        context = ContextSerialization(
            self._plugin_id, version_table, packet_debugging)
        context.write_uint(request_id)
        command_hash = CommandCallbacks.Hashes.MessageHashes[message_type]
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
        return command_hash == CommandCallbacks.Hashes.CommandHashes[CommandCallbacks.Commands.connect]

    def __init__(self):
        self._plugin_id = 0

# -------------Commands----------- #
# Commands are incoming (nanome -> plugin)


def add_command(command, serializer, callback):
    Serializer._commands[CommandCallbacks.Hashes.CommandHashes[command]] = serializer
    Serializer._command_callbacks[CommandCallbacks.Hashes.CommandHashes[command]] = callback


# control
add_command(CommandCallbacks.Commands.connect,
            CommandSerializers.Connect(), CommandCallbacks._connect)
add_command(CommandCallbacks.Commands.run,
            CommandSerializers.Run(), CommandCallbacks._run)
add_command(CommandCallbacks.Commands.advanced_settings,
            CommandSerializers.AdvancedSettings(), CommandCallbacks._advanced_settings)

# workspace
add_command(CommandCallbacks.Commands.workspace_response,
            CommandSerializers.ReceiveWorkspace(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.complex_add,
            CommandSerializers.ComplexAddedRemoved(), CommandCallbacks._complex_added)
add_command(CommandCallbacks.Commands.complex_remove,
            CommandSerializers.ComplexAddedRemoved(), CommandCallbacks._complex_removed)
add_command(CommandCallbacks.Commands.complex_list_response,
            CommandSerializers.ReceiveComplexList(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.complexes_response,
            CommandSerializers.ReceiveComplexes(), CommandCallbacks._receive_complexes)
add_command(CommandCallbacks.Commands.structures_deep_update_done,
            CommandSerializers.UpdateStructuresDeepDone(), CommandCallbacks._simple_callback_no_arg)
add_command(CommandCallbacks.Commands.add_to_workspace_done,
            CommandSerializers.AddToWorkspace(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.position_structures_done,
            CommandSerializers.PositionStructuresDone(), CommandCallbacks._simple_callback_no_arg)
add_command(CommandCallbacks.Commands.dssp_add_done,
            CommandSerializers.AddDSSP(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.bonds_add_done,
            CommandSerializers.AddBonds(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.complex_updated,
            CommandSerializers.ComplexUpdated(), CommandCallbacks._complex_updated)
add_command(CommandCallbacks.Commands.selection_changed,
            CommandSerializers.SelectionChanged(), CommandCallbacks._selection_changed)
add_command(CommandCallbacks.Commands.compute_hbonds_done,
            CommandSerializers.ComputeHBonds(), CommandCallbacks._simple_callback_no_arg)
add_command(CommandCallbacks.Commands.substructure_response,
            CommandSerializers.RequestSubstructure(), CommandCallbacks._simple_callback_arg)

# Volume
add_command(CommandCallbacks.Commands.add_volume_done,
            CommandSerializers.AddVolumeDone(), CommandCallbacks._simple_callback_no_arg)

# ui
add_command(CommandCallbacks.Commands.menu_toggle,
            CommandSerializers.MenuCallback(), CommandCallbacks._menu_toggled)
add_command(CommandCallbacks.Commands.button_press,
            CommandSerializers.ButtonCallback(), CommandCallbacks._button_pressed)
add_command(CommandCallbacks.Commands.button_hover,
            CommandSerializers.ButtonCallback(), CommandCallbacks._button_hover)
add_command(CommandCallbacks.Commands.slider_release,
            CommandSerializers.SliderCallback(), CommandCallbacks._slider_released)
add_command(CommandCallbacks.Commands.slider_change,
            CommandSerializers.SliderCallback(), CommandCallbacks._slider_changed)
add_command(CommandCallbacks.Commands.text_submit,
            CommandSerializers.TextInputCallback(), CommandCallbacks._text_submit)
add_command(CommandCallbacks.Commands.text_change,
            CommandSerializers.TextInputCallback(), CommandCallbacks._text_changed)
add_command(CommandCallbacks.Commands.image_press,
            CommandSerializers.ImageCallback(), CommandCallbacks._image_pressed)
add_command(CommandCallbacks.Commands.image_hold,
            CommandSerializers.ImageCallback(), CommandCallbacks._image_held)
add_command(CommandCallbacks.Commands.image_release,
            CommandSerializers.ImageCallback(), CommandCallbacks._image_released)
add_command(CommandCallbacks.Commands.dropdown_item_click,
            CommandSerializers.DropdownCallback(), CommandCallbacks._dropdown_item_clicked)
add_command(CommandCallbacks.Commands.menu_transform_response,
            CommandSerializers.GetMenuTransformResponse(), CommandCallbacks._simple_callback_arg_unpack)

# files
add_command(CommandCallbacks.Commands.export_files_result,
            CommandSerializers.ExportFiles(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.print_working_directory_response,
            CommandSerializers.PWD(), CommandCallbacks._simple_callback_arg_unpack)
add_command(CommandCallbacks.Commands.cd_response,
            CommandSerializers.CD(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.ls_response, CommandSerializers.LS(
), CommandCallbacks._simple_callback_arg_unpack)
add_command(CommandCallbacks.Commands.mv_response,
            CommandSerializers.MV(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.cp_response,
            CommandSerializers.CP(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.get_response, CommandSerializers.Get(
), CommandCallbacks._simple_callback_arg_unpack)
add_command(CommandCallbacks.Commands.put_response,
            CommandSerializers.Put(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.rm_response,
            CommandSerializers.RM(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.rmdir_response,
            CommandSerializers.RMDir(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.mkdir_response,
            CommandSerializers.MKDir(), CommandCallbacks._simple_callback_arg)

# streams
add_command(CommandCallbacks.Commands.stream_create_done,
            CommandSerializers.CreateStreamResult(), CommandCallbacks._receive_create_stream_result)
add_command(CommandCallbacks.Commands.stream_feed,
            CommandSerializers.FeedStream(), CommandCallbacks._feed_stream)
add_command(CommandCallbacks.Commands.stream_interrupt,
            CommandSerializers.InterruptStream(), CommandCallbacks._receive_interrupt_stream)
add_command(CommandCallbacks.Commands.stream_feed_done,
            CommandSerializers.FeedStreamDone(), CommandCallbacks._simple_callback_no_arg)

# macros
add_command(CommandCallbacks.Commands.get_macros_response,
            CommandSerializers.GetMacrosResponse(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.run_macro_result,
            CommandSerializers.RunMacro(), CommandCallbacks._simple_callback_arg)

# Presenter
add_command(CommandCallbacks.Commands.presenter_info_response,
            CommandSerializers.GetPresenterInfoResponse(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.presenter_change,
            CommandSerializers.PresenterChange(), CommandCallbacks._presenter_change)
add_command(CommandCallbacks.Commands.controller_transforms_response,
            CommandSerializers.GetControllerTransformsResponse(), CommandCallbacks._simple_callback_arg_unpack)

# Shape
add_command(CommandCallbacks.Commands.set_shape_result,
            CommandSerializers.SetShape(), CommandCallbacks._simple_callback_arg_unpack)
add_command(CommandCallbacks.Commands.delete_shape_result,
            CommandSerializers.DeleteShape(), CommandCallbacks._simple_callback_arg)

# others
add_command(CommandCallbacks.Commands.load_file_done,
            CommandSerializers.LoadFileDone(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.integration,
            CommandSerializers.Integration(), CommandCallbacks._integration)

# -------------Messages----------- #
# Messages are outgoing (plugin -> nanome)


def add_message(command, serializer):
    Serializer._messages[CommandCallbacks.Hashes.MessageHashes[command]] = serializer


Serializers.type_serializer.TypeSerializer.register_string_raw(
    MESSAGE_VERSION_KEY, 1)
# control
add_message(CommandCallbacks.Messages.connect, CommandSerializers.Connect())

# workspace
add_message(CommandCallbacks.Messages.workspace_update,
            CommandSerializers.UpdateWorkspace())
add_message(CommandCallbacks.Messages.structures_deep_update,
            CommandSerializers.UpdateStructures(False))
add_message(CommandCallbacks.Messages.structures_shallow_update,
            CommandSerializers.UpdateStructures(True))
add_message(CommandCallbacks.Messages.workspace_request,
            CommandSerializers.RequestWorkspace())
add_message(CommandCallbacks.Messages.complex_list_request,
            CommandSerializers.RequestComplexList())
add_message(CommandCallbacks.Messages.add_to_workspace,
            CommandSerializers.AddToWorkspace())
add_message(CommandCallbacks.Messages.complexes_request,
            CommandSerializers.RequestComplexes())
add_message(CommandCallbacks.Messages.bonds_add,
            CommandSerializers.AddBonds())
add_message(CommandCallbacks.Messages.dssp_add, CommandSerializers.AddDSSP())
add_message(CommandCallbacks.Messages.structures_zoom,
            CommandSerializers.PositionStructures())
add_message(CommandCallbacks.Messages.structures_center,
            CommandSerializers.PositionStructures())
add_message(CommandCallbacks.Messages.hook_complex_updated,
            CommandSerializers.ComplexUpdatedHook())
add_message(CommandCallbacks.Messages.hook_selection_changed,
            CommandSerializers.SelectionChangedHook())
add_message(CommandCallbacks.Messages.compute_hbonds,
            CommandSerializers.ComputeHBonds())
add_message(CommandCallbacks.Messages.substructure_request,
            CommandSerializers.RequestSubstructure())

# volume
add_message(CommandCallbacks.Messages.add_volume,
            CommandSerializers.AddVolume())

# ui
add_message(CommandCallbacks.Messages.menu_update,
            CommandSerializers.UpdateMenu())
add_message(CommandCallbacks.Messages.content_update,
            CommandSerializers.UpdateContent())
add_message(CommandCallbacks.Messages.node_update,
            CommandSerializers.UpdateNode())
add_message(CommandCallbacks.Messages.menu_transform_set,
            CommandSerializers.SetMenuTransform())
add_message(CommandCallbacks.Messages.menu_transform_request,
            CommandSerializers.GetMenuTransform())
add_message(CommandCallbacks.Messages.notification_send,
            CommandSerializers.SendNotification())
add_message(CommandCallbacks.Messages.hook_ui_callback,
            CommandSerializers.UIHook())

# files
add_message(CommandCallbacks.Messages.print_working_directory,
            CommandSerializers.PWD())
add_message(CommandCallbacks.Messages.cd, CommandSerializers.CD())
add_message(CommandCallbacks.Messages.ls, CommandSerializers.LS())
add_message(CommandCallbacks.Messages.mv, CommandSerializers.MV())
add_message(CommandCallbacks.Messages.cp, CommandSerializers.CP())
add_message(CommandCallbacks.Messages.get, CommandSerializers.Get())
add_message(CommandCallbacks.Messages.put, CommandSerializers.Put())
add_message(CommandCallbacks.Messages.rm, CommandSerializers.RM())
add_message(CommandCallbacks.Messages.rmdir, CommandSerializers.RMDir())
add_message(CommandCallbacks.Messages.mkdir, CommandSerializers.MKDir())

# macros
add_message(CommandCallbacks.Messages.run_macro,
            CommandSerializers.RunMacro())
add_message(CommandCallbacks.Messages.save_macro,
            CommandSerializers.SaveMacro())
add_message(CommandCallbacks.Messages.delete_macro,
            CommandSerializers.DeleteMacro())
add_message(CommandCallbacks.Messages.get_macros,
            CommandSerializers.GetMacros())
add_message(CommandCallbacks.Messages.stop_macro,
            CommandSerializers.StopMacro())

# streams
add_message(CommandCallbacks.Messages.stream_create,
            CommandSerializers.CreateStream())
add_message(CommandCallbacks.Messages.stream_feed,
            CommandSerializers.FeedStream())
add_message(CommandCallbacks.Messages.stream_destroy,
            CommandSerializers.DestroyStream())

# Presenter
add_message(CommandCallbacks.Messages.presenter_info_request,
            CommandSerializers.GetPresenterInfo())
add_message(CommandCallbacks.Messages.controller_transforms_request,
            CommandSerializers.GetControllerTransforms())

# Shape
add_message(CommandCallbacks.Messages.set_shape,
            CommandSerializers.SetShape())
add_message(CommandCallbacks.Messages.delete_shape,
            CommandSerializers.DeleteShape())

# others
add_message(CommandCallbacks.Messages.open_url, CommandSerializers.OpenURL())
add_message(CommandCallbacks.Messages.load_file,
            CommandSerializers.LoadFile())
add_message(CommandCallbacks.Messages.integration,
            CommandSerializers.Integration())
add_message(CommandCallbacks.Messages.set_skybox,
            CommandSerializers.SetSkybox())
add_message(CommandCallbacks.Messages.apply_color_scheme,
            CommandSerializers.ApplyColorScheme())

# files deprecated
add_message(CommandCallbacks.Messages.directory_request,
            CommandSerializers.DirectoryRequest())
add_message(CommandCallbacks.Messages.file_request,
            CommandSerializers.FileRequest())
add_message(CommandCallbacks.Messages.file_save,
            CommandSerializers.FileSave())
add_message(CommandCallbacks.Messages.export_files,
            CommandSerializers.ExportFiles())
add_message(CommandCallbacks.Messages.plugin_list_button_set,
            CommandSerializers.SetPluginListButton())
add_command(CommandCallbacks.Commands.directory_response,
            CommandSerializers.DirectoryRequest(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.file_response,
            CommandSerializers.FileRequest(), CommandCallbacks._simple_callback_arg)
add_command(CommandCallbacks.Commands.file_save_done,
            CommandSerializers.FileSave(), CommandCallbacks._simple_callback_arg)
