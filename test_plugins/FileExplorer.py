import nanome
import os
from nanome.api.ui import Menu
from nanome.api.ui import LayoutNode

NAME = "File Explorer"
DESCRIPTION = "Allows you to browse your files"
CATEGORY = ""
HAS_ADVANCED_OPTIONS = False

test_assets = os.getcwd() + ("/testing/test_assets")


class FileExplorer(nanome.PluginInstance):

    def __init__(self):
        self.item_prefab = LayoutNode.io.from_json(test_assets + "/File.json")
        self.menu = Menu.io.from_json(test_assets + "/FileExplorer.json")
        self.grid = self.menu.root.find_node("Grid", True).get_content()
        self.selected_button = None

    def run(self):
        self.request_directory(".", self.on_directory_received)

    def on_directory_received(self, result):
        if result.error_code != nanome.util.DirectoryErrorCode.no_error: # If API couldn't access directory, display error
            nanome.util.Logs.error("Directory request error:", str(result.error_code))
            return

        self.grid.items = []
        for entry in result.entry_array:
            self.create_file_rep(entry)

        #self.request_files(["./api_bad_test.txt", "api_test.txt"], self.on_files_received) # Read two files

    def create_file_rep(self, entry):
        item = self.item_prefab.clone()
        button = item.find_node("Button", True).get_content()
        button.register_pressed_callback(self.entry_pressed)
        button.entry = entry
        button.text.value.set_all(entry.name)

    def entry_pressed(self, button):
        button.selected = True
        if self.selected_button is not None:
            self.selected_button.selected = False
        self.selected_button = button

    def load_pressed(self, button):
        pass

    def save_pressed(self, button):
        pass

    def back_pressed(self, button):
        pass

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, FileExplorer)