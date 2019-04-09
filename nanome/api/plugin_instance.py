from nanome.util import Logs, DirectoryRequestOptions, IntEnum
from nanome._internal import _PluginInstance
from nanome._internal._network import _ProcessNetwork
from nanome._internal._network._commands._callbacks import _Messages

import inspect
import sys

class PluginInstance(_PluginInstance):

    """
    | Base class of any Plugin class.
    | Constructor should never be called by the user as it is instantiated by network, when a session connects.
    | Start, update, and all methods starting by "on" can be overridden by user, in order to get requests results
    """
    def __init__(self):
        super(_PluginInstance, self).__init__()

    def start(self):
        """
        | Called when user "Activates" the plugin
        """
        pass

    def update(self):
        """
        | Called when when instance updates (multiple times per second)
        """
        pass

    def on_run(self):
        """
        | Called when user presses "Run"
        """
        Logs.warning('Callback on_run not defined. Ignoring')

    def on_advanced_settings(self):
        """
        | Called when user presses "Advanced Settings"
        """
        Logs.warning('Callback on_advanced_settings not defined. Ignoring')

    def on_complex_added(self):
        """
        | Called whenever a complex is added to the workspace.
        """
        Logs.warning('Callback on_complex_added not defined. Ignoring')

    def on_complex_removed(self):
        """
        | Called whenever a complex is removed from the workspace.
        """
        Logs.warning('Callback on_complex_removed not defined. Ignoring')

    def request_workspace(self, callback = None):
        """
        | Request the entire workspace, in deep mode
        """
        id = self._network._send(_Messages.request_workspace)
        self.__save_callback(id, callback)

    def request_complex_list(self, callback = None):
        """
        | Request the list of all complexes in the workspace, in shallow mode
        """
        id = self._network._send(_Messages.request_complex_list)
        self.__save_callback(id, callback)

    def request_complexes(self, id_list, callback = None):
        """
        | Requests a list of complexes by their indices
        | Complexes returned contains the full structure (atom/bond/residue/chain/molecule)

        :param id_list: List of indices
        :type id_list: list of :class:`int`
        """
        id = self._network._send(_Messages.request_complexes, id_list)
        self.__save_callback(id, callback)

    def update_workspace(self, workspace):
        """
        | Replace the current workspace in the scene by the workspace in parameter

        :param workspace: New workspace
        :type workspace: :class:`~nanome.api.structure.workspace.Workspace`
        """
        self._network._send(_Messages.update_workspace, workspace)

    def send_notification(self, type, message):
        """
        | Send a notification to the user

        :param type: Type of notification to send.
        :type workspace: :class:`~nanome.util.notification_types.NotificationTypes`
        :param message: Text to display to the user.
        :type message: str
        """
        #avoids unnecessary dependencies.
        #needs to match the command serializer.
        args = (type, message)
        self._network._send(_Messages.send_notification, args)

    def update_structures_deep(self, structures):
        """
        | Update the specific molecular structures in the scene to match the structures in parameter.
        | Will also update descendent structures and can be used to remove descendent structures.

        :param structures: List of molecular structures to update.
        :type structures: list of :class:`~nanome.api.structure.base.Base`
        """
        self._network._send(_Messages.update_structures_deep, structures)

    def update_structures_shallow(self, structures):
        """
        | Update the specific molecular structures in the scene to match the structures in parameter
        | Only updates the structure's data, will not update children or other descendents.

        :param structures: List of molecular structures to update.
        :type structures: list of :class:`~nanome.api.structure.base.Base`
        """
        self._network._send(_Messages.update_structures_shallow, structures)

    def add_to_workspace(self, complex_list):
        """
        | Add a list of complexes to the current workspace

        :param complex_list: List of Complexes to add
        :type complex_list: list of :class:`~nanome.api.structure.complex.Complex`
        """
        self._network._send(_Messages.add_to_workspace, complex_list)

    def update_menu(self, menu):
        """
        | Update the menu in Nanome

        :param menu: Menu to update
        :type menu: :class:`~nanome.api.ui.menu.Menu`
        """
        self._network._send(_Messages.update_menu, menu)
        
    def update_content(self, content):
        """
        | Update a specific UI element (button, slider, list...)

        :param content: UI element to update
        :type content: :class:`~nanome.api.ui.ui_base`
        """
        self._network._send(_Messages.update_content, content)

    def request_directory(self, path, callback = None, pattern = "*"):
        """
        | Requests the content of a directory on the machine running Nanome

        :param path: Path to request. E.g. "." means Nanome's running directory
        :type path: str
        :param pattern: Pattern to match. E.g. "*.txt" will match all .txt files. Default value is "*" (match everything)
        :type pattern: str
        """
        options = DirectoryRequestOptions()
        options._directory_name = path
        options._pattern = pattern
        id = self._network._send(_Messages.request_directory, options)
        self.__save_callback(id, callback)

    def request_files(self, file_list, callback = None):
        """
        | Reads files on the machine running Nanome, and returns them

        :param file_list: List of file name (with path) to read. E.g. ["a.sdf", "../b.sdf"] will read a.sdf in running directory, b.sdf in parent directory, and return them
        :type file_list: list of :class:`str`
        """
        id = self._network._send(_Messages.request_file, file_list)
        self.__save_callback(id, callback)

    def save_files(self, file_list, callback = None):
        """
        | Save files on the machine running Nanome, and returns result

        :param file_list: List of files to save with their content
        :type file_list: list of :class:`~nanome.util.file.FileSaveData`
        """
        id = self._network._send(_Messages.save_file, file_list)
        self.__save_callback(id, callback)

    

    def __save_callback(self, id, callback):
        if callback == None:
            _PluginInstance.__callbacks[id] = lambda res : None
        else:
            _PluginInstance.__callbacks[id] = callback

    class PluginListButtonType(IntEnum):
        run = 0
        advanced_settings = 1

    def set_plugin_list_button(self, button, text = None, usable = None):
        """
        | Set text and/or usable state of the buttons on the plugin connection menu in Nanome

        :param button: Button to set
        :type button: :class:`~ButtonType`
        :param text: Text displayed on the button. If None, doesn't set text
        :type text: str
        :param usable: Set button to be usable or not. If None, doesn't set usable text
        :type usable: bool
        """
        if button == PluginInstance.PluginListButtonType.run:
            current_text = [self._run_text]
            current_usable = [self._run_usable]
        else:
            current_text = [self._advanced_settings_text]
            current_usable = [self._advanced_settings_usable]
        
        if text == None:
            text = current_text[0]
        else:
            current_text[0] = text
        if usable == None:
            usable = current_usable[0]
        else:
            current_usable[0] = usable

        self._network._send(_Messages.set_plugin_list_button, (button, text, usable))
        
class _DefaultPlugin(PluginInstance):
    def __init__(self):
        pass