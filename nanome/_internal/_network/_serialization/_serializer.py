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
        context.write_uint(message_type)
        if arg != None:
            try:
                command = Serializer._messages[message_type]
                context.write_using_serializer(command, arg)
                return context.to_array()
            except KeyError:
                Logs.warning("Trying to serialize an unregistered message type:", message_type)
        return context.to_array()

    def deserialize_command(self, payload, version_table):
        context = _ContextDeserialization(payload, version_table, packet_debugging)
        try:
            request_id = context.read_uint()
            command_id = context.read_uint()
            command = Serializer._commands[command_id]
        except KeyError:
            if self.try_register_session(payload) == True:
                Logs.error("A session is trying to connect even though it is already connected")
            else:
                Logs.error("Received an unregistered command:", command_id)
            return
        except BufferError as err:
            Logs.error(err)
            return None
        except struct.error as err:
            Logs.error(err)
            return None

        try:
            received_object = context.read_using_serializer(command)
        except BufferError as err:
            Logs.error(err)
            return None
        except struct.error as err:
            Logs.error(err)
            return None
        return received_object, command_id, request_id

    def try_register_session(self, payload):
        context = _ContextDeserialization(payload, None, packet_debugging)
        context.read_uint()
        command_id = context.read_uint()
        return command_id == CommandCallbacks._Commands.connect

    def __init__(self):
        pass
#-------------Commands-----------#
# Commands are incoming (nanome -> plugin)

#basic


#control
Serializer._commands[CommandCallbacks._Commands.connect] = CommandSerializers._Connect()
Serializer._commands[CommandCallbacks._Commands.run] = CommandSerializers._Run()
Serializer._commands[CommandCallbacks._Commands.advanced_settings] = CommandSerializers._AdvancedSettings()

#workspace
Serializer._commands[CommandCallbacks._Commands.receive_workspace] = CommandSerializers._ReceiveWorkspace()
Serializer._commands[CommandCallbacks._Commands.complex_added] = CommandSerializers._ComplexAddedRemoved()
Serializer._commands[CommandCallbacks._Commands.complex_removed] = CommandSerializers._ComplexAddedRemoved()
Serializer._commands[CommandCallbacks._Commands.receive_complex_list] = CommandSerializers._ReceiveComplexList()
Serializer._commands[CommandCallbacks._Commands.receive_complexes] = CommandSerializers._ReceiveComplexes()

#ui
Serializer._commands[CommandCallbacks._Commands.menu_toggled] = CommandSerializers._MenuCallback()
Serializer._commands[CommandCallbacks._Commands.button_pressed] = CommandSerializers._ButtonCallback()
Serializer._commands[CommandCallbacks._Commands.slider_released] = CommandSerializers._SliderCallback()
Serializer._commands[CommandCallbacks._Commands.slider_changed] = CommandSerializers._SliderCallback()
Serializer._commands[CommandCallbacks._Commands.text_submit] = CommandSerializers._TextInputCallback()
Serializer._commands[CommandCallbacks._Commands.text_changed] = CommandSerializers._TextInputCallback()

#file
Serializer._commands[CommandCallbacks._Commands.receive_directory] = CommandSerializers._DirectoryRequest()
Serializer._commands[CommandCallbacks._Commands.receive_file] = CommandSerializers._FileRequest()
Serializer._commands[CommandCallbacks._Commands.receive_file_save_result] = CommandSerializers._FileSave()

#-------------Messages-----------#
# Messages are outgoing (plugin -> nanome)

#basic

#control
Serializer._messages[CommandCallbacks._Messages.connect] = CommandSerializers._Connect()

#workspace
Serializer._messages[CommandCallbacks._Messages.send_notification] = CommandSerializers._SendNotification()
Serializer._messages[CommandCallbacks._Messages.update_workspace] = CommandSerializers._UpdateWorkspace()
Serializer._messages[CommandCallbacks._Messages.update_structures_deep] = CommandSerializers._UpdateStructures(False)
Serializer._messages[CommandCallbacks._Messages.update_structures_shallow] = CommandSerializers._UpdateStructures(True)
Serializer._messages[CommandCallbacks._Messages.request_workspace] = CommandSerializers._RequestWorkspace()
Serializer._messages[CommandCallbacks._Messages.request_complex_list] = CommandSerializers._RequestComplexList()
Serializer._messages[CommandCallbacks._Messages.add_to_workspace] = CommandSerializers._AddToWorkspace()
Serializer._messages[CommandCallbacks._Messages.request_complexes] = CommandSerializers._RequestComplexes()

#ui
Serializer._messages[CommandCallbacks._Messages.update_menu] = CommandSerializers._UpdateMenu()
Serializer._messages[CommandCallbacks._Messages.update_content] = CommandSerializers._UpdateContent()

#file
Serializer._messages[CommandCallbacks._Messages.request_directory] = CommandSerializers._DirectoryRequest()
Serializer._messages[CommandCallbacks._Messages.request_file] = CommandSerializers._FileRequest()
Serializer._messages[CommandCallbacks._Messages.save_file] = CommandSerializers._FileSave()
Serializer._messages[CommandCallbacks._Messages.set_plugin_list_button] = CommandSerializers._SetPluginListButton()

#-------------Callbacks-----------#
# Callbacks are things to do after the command is decoded (plugin -> plugin)

#basic

#control
Serializer._command_callbacks[CommandCallbacks._Commands.connect] = CommandCallbacks._connect
Serializer._command_callbacks[CommandCallbacks._Commands.run] = CommandCallbacks._run
Serializer._command_callbacks[CommandCallbacks._Commands.advanced_settings] = CommandCallbacks._advanced_settings

#workspace
Serializer._command_callbacks[CommandCallbacks._Commands.receive_complex_list] = CommandCallbacks._receive_complex_list
Serializer._command_callbacks[CommandCallbacks._Commands.receive_workspace] = CommandCallbacks._receive_workspace
Serializer._command_callbacks[CommandCallbacks._Commands.complex_added] = CommandCallbacks._complex_added
Serializer._command_callbacks[CommandCallbacks._Commands.complex_removed] = CommandCallbacks._complex_removed

#ui
Serializer._command_callbacks[CommandCallbacks._Commands.receive_menu] = CommandCallbacks._receive_menu
Serializer._command_callbacks[CommandCallbacks._Commands.menu_toggled] = CommandCallbacks._menu_toggled
Serializer._command_callbacks[CommandCallbacks._Commands.slider_released] = CommandCallbacks._slider_released
Serializer._command_callbacks[CommandCallbacks._Commands.slider_changed] = CommandCallbacks._slider_changed
Serializer._command_callbacks[CommandCallbacks._Commands.text_submit] = CommandCallbacks._text_submit
Serializer._command_callbacks[CommandCallbacks._Commands.text_changed] = CommandCallbacks._text_changed
Serializer._command_callbacks[CommandCallbacks._Commands.button_pressed] = CommandCallbacks._button_pressed
Serializer._command_callbacks[CommandCallbacks._Commands.receive_complexes] = CommandCallbacks._receive_complexes

#file
Serializer._command_callbacks[CommandCallbacks._Commands.receive_directory] = CommandCallbacks._receive_directory
Serializer._command_callbacks[CommandCallbacks._Commands.receive_file] = CommandCallbacks._receive_file
Serializer._command_callbacks[CommandCallbacks._Commands.receive_file_save_result] = CommandCallbacks._receive_file_save_result
