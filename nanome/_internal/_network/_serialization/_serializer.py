from . import _ContextSerialization, _ContextDeserialization
from .._commands import _callbacks as CommandCallbacks
from .._commands import _serialization as CommandSerializers
from nanome._internal._util import _serializers as Serializers
from nanome.util import Logs
import struct

packet_debugging = False

class Serializer(object):
    _commands = dict()
    _messages = dict()
    _command_callbacks = dict()

    def serialize_message(self, request_id, message_type, arg, version_table):
        context = _ContextSerialization(version_table, packet_debugging)
        context.write_uint(request_id)
        command_hash = CommandCallbacks._Hashes.MessageHashes[message_type]
        context.write_uint(command_hash)
        if arg != None:
            command = None
            try:
                command = Serializer._messages[command_hash]
            except KeyError:
                Logs.warning("Trying to serialize an unregistered message type:", message_type)
            if command != None:
                context.write_using_serializer(command, arg)
                return context.to_array()
        return context.to_array()

    def deserialize_command(self, payload, version_table):
        context = _ContextDeserialization(payload, version_table, packet_debugging)
        try:
            request_id = context.read_uint()
            command_hash = context.read_uint()
            command = Serializer._commands[command_hash]
        except KeyError:
            if self.try_register_session(payload) == True:
                Logs.error("A session is trying to connect even though it is already connected")
            else:
                Logs.error("Received an unregistered command:", command_hash)
            return (None, None, None)
        except BufferError as err:
            Logs.error(err)
            return (None, None, None)
        except struct.error as err:
            Logs.error(err)
            return (None, None, None)

        try:
            received_object = context.read_using_serializer(command)
        except BufferError as err:
            Logs.error(err)
            return (None, None, None)
        except struct.error as err:
            Logs.error(err)
            return (None, None, None)
        return received_object, command_hash, request_id

    def try_register_session(self, payload):
        context = _ContextDeserialization(payload, None, packet_debugging)
        context.read_uint() # Read the request ID
        command_hash = context.read_uint()
        return command_hash == CommandCallbacks._Hashes.CommandHashes[CommandCallbacks._Commands.connect]

    def __init__(self):
        pass
#-------------Commands-----------#
# Commands are incoming (nanome -> plugin)

def add_command(command, serializer):
    Serializer._commands[CommandCallbacks._Hashes.CommandHashes[command]] = serializer

#basic


#control
add_command(CommandCallbacks._Commands.connect, CommandSerializers._Connect())
add_command(CommandCallbacks._Commands.run, CommandSerializers._Run())
add_command(CommandCallbacks._Commands.advanced_settings, CommandSerializers._AdvancedSettings())

#workspace
add_command(CommandCallbacks._Commands.workspace_receive, CommandSerializers._ReceiveWorkspace())
add_command(CommandCallbacks._Commands.complex_add, CommandSerializers._ComplexAddedRemoved())
add_command(CommandCallbacks._Commands.complex_remove, CommandSerializers._ComplexAddedRemoved())
add_command(CommandCallbacks._Commands.complex_list_receive, CommandSerializers._ReceiveComplexList())
add_command(CommandCallbacks._Commands.complexes_receive, CommandSerializers._ReceiveComplexes())
add_command(CommandCallbacks._Commands.structures_deep_update_done, CommandSerializers._UpdateStructuresDeepDone())
add_command(CommandCallbacks._Commands.position_structures_done, CommandSerializers._PositionStructuresDone())
add_command(CommandCallbacks._Commands.bonds_add_result, CommandSerializers._AddBonds())

#ui
add_command(CommandCallbacks._Commands.menu_toggle, CommandSerializers._MenuCallback())
add_command(CommandCallbacks._Commands.button_press, CommandSerializers._ButtonCallback())
add_command(CommandCallbacks._Commands.slider_release, CommandSerializers._SliderCallback())
add_command(CommandCallbacks._Commands.slider_change, CommandSerializers._SliderCallback())
add_command(CommandCallbacks._Commands.text_submit, CommandSerializers._TextInputCallback())
add_command(CommandCallbacks._Commands.text_change, CommandSerializers._TextInputCallback())
add_command(CommandCallbacks._Commands.image_press, CommandSerializers._ImageCallback())
add_command(CommandCallbacks._Commands.image_hold, CommandSerializers._ImageCallback())
add_command(CommandCallbacks._Commands.image_release, CommandSerializers._ImageCallback())

#file
add_command(CommandCallbacks._Commands.directory_receive, CommandSerializers._DirectoryRequest())
add_command(CommandCallbacks._Commands.file_receive, CommandSerializers._FileRequest())
add_command(CommandCallbacks._Commands.file_save_result_receive, CommandSerializers._FileSave())

#streams
add_command(CommandCallbacks._Commands.stream_create_result,CommandSerializers._CreateStreamResult())
add_command(CommandCallbacks._Commands.stream_interrupt, CommandSerializers._InterruptStream())
add_command(CommandCallbacks._Commands.stream_feed_done, CommandSerializers._FeedStreamDone())

#-------------Messages-----------#
# Messages are outgoing (plugin -> nanome)

def add_message(command, serializer):
    Serializer._messages[CommandCallbacks._Hashes.MessageHashes[command]] = serializer

#basic

#control
add_message(CommandCallbacks._Messages.connect, CommandSerializers._Connect())

#workspace
add_message(CommandCallbacks._Messages.workspace_update, CommandSerializers._UpdateWorkspace())
add_message(CommandCallbacks._Messages.structures_deep_update, CommandSerializers._UpdateStructures(False))
add_message(CommandCallbacks._Messages.structures_shallow_update, CommandSerializers._UpdateStructures(True))
add_message(CommandCallbacks._Messages.workspace_request, CommandSerializers._RequestWorkspace())
add_message(CommandCallbacks._Messages.complex_list_request, CommandSerializers._RequestComplexList())
add_message(CommandCallbacks._Messages.add_to_workspace, CommandSerializers._AddToWorkspace())
add_message(CommandCallbacks._Messages.complexes_request, CommandSerializers._RequestComplexes())
add_message(CommandCallbacks._Messages.bonds_add, CommandSerializers._AddBonds())
add_message(CommandCallbacks._Messages.structures_zoom, CommandSerializers._PositionStructures())
add_message(CommandCallbacks._Messages.structures_center, CommandSerializers._PositionStructures())

#ui
add_message(CommandCallbacks._Messages.menu_update, CommandSerializers._UpdateMenu())
add_message(CommandCallbacks._Messages.content_update, CommandSerializers._UpdateContent())
add_message(CommandCallbacks._Messages.notification_send, CommandSerializers._SendNotification())

#file
add_message(CommandCallbacks._Messages.directory_request, CommandSerializers._DirectoryRequest())
add_message(CommandCallbacks._Messages.file_request, CommandSerializers._FileRequest())
add_message(CommandCallbacks._Messages.file_save, CommandSerializers._FileSave())
add_message(CommandCallbacks._Messages.plugin_list_button_set, CommandSerializers._SetPluginListButton())

#streams
add_message(CommandCallbacks._Messages.stream_create, CommandSerializers._CreateStream())
add_message(CommandCallbacks._Messages.stream_feed, CommandSerializers._FeedStream())
add_message(CommandCallbacks._Messages.stream_destroy, CommandSerializers._DestroyStream())

#-------------Callbacks-----------#
# Callbacks are things to do after the command is decoded (plugin -> plugin)

def add_callback(command, callback):
    Serializer._command_callbacks[CommandCallbacks._Hashes.CommandHashes[command]] = callback

#basic

#control
add_callback(CommandCallbacks._Commands.connect, CommandCallbacks._connect)
add_callback(CommandCallbacks._Commands.run, CommandCallbacks._run)
add_callback(CommandCallbacks._Commands.advanced_settings, CommandCallbacks._advanced_settings)

#workspace
add_callback(CommandCallbacks._Commands.complex_list_receive, CommandCallbacks._receive_complex_list)
add_callback(CommandCallbacks._Commands.workspace_receive, CommandCallbacks._receive_workspace)
add_callback(CommandCallbacks._Commands.complex_add, CommandCallbacks._complex_added)
add_callback(CommandCallbacks._Commands.complex_remove, CommandCallbacks._complex_removed)
add_callback(CommandCallbacks._Commands.structures_deep_update_done, CommandCallbacks._update_structures_deep_done)
add_callback(CommandCallbacks._Commands.position_structures_done, CommandCallbacks._position_structures_done)
add_callback(CommandCallbacks._Commands.bonds_add_result, CommandCallbacks._add_bonds_result)
add_callback(CommandCallbacks._Commands.complexes_receive, CommandCallbacks._receive_complexes)

#ui
add_callback(CommandCallbacks._Commands.menu_receive, CommandCallbacks._receive_menu)
add_callback(CommandCallbacks._Commands.menu_toggle, CommandCallbacks._menu_toggled)
add_callback(CommandCallbacks._Commands.slider_release, CommandCallbacks._slider_released)
add_callback(CommandCallbacks._Commands.slider_change, CommandCallbacks._slider_changed)
add_callback(CommandCallbacks._Commands.text_submit, CommandCallbacks._text_submit)
add_callback(CommandCallbacks._Commands.text_change, CommandCallbacks._text_changed)
add_callback(CommandCallbacks._Commands.button_press, CommandCallbacks._button_pressed)
add_callback(CommandCallbacks._Commands.image_press, CommandCallbacks._image_pressed)
add_callback(CommandCallbacks._Commands.image_hold, CommandCallbacks._image_held)
add_callback(CommandCallbacks._Commands.image_release, CommandCallbacks._image_released)

#file
add_callback(CommandCallbacks._Commands.directory_receive, CommandCallbacks._receive_directory)
add_callback(CommandCallbacks._Commands.file_receive, CommandCallbacks._receive_file)
add_callback(CommandCallbacks._Commands.file_save_result_receive, CommandCallbacks._receive_file_save_result)

#streams
add_callback(CommandCallbacks._Commands.stream_create_result, CommandCallbacks._receive_create_stream_result)
add_callback(CommandCallbacks._Commands.stream_interrupt, CommandCallbacks._receive_interrupt_stream)
add_callback(CommandCallbacks._Commands.stream_feed_done, CommandCallbacks._feed_stream_done)
