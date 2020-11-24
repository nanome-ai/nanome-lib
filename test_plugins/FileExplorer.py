import nanome
import os
import tempfile
from nanome.api.ui import Menu
from nanome.api.ui import LayoutNode

NAME = "File Explorer"
DESCRIPTION = "Allows you to browse your files"
CATEGORY = ""
HAS_ADVANCED_OPTIONS = False

test_assets = os.getcwd() + ("/testing/test_assets")


class FileExplorer(nanome.PluginInstance):

    def __init__(self):
        self.running = False
        self.item_prefab = LayoutNode.io.from_json(test_assets + "/File.json")
        self.menu = Menu.io.from_json(test_assets + "/FileExplorer.json")
        self.grid = self.menu.root.find_node("Grid", True).get_content()
        self.path_text = self.menu.root.find_node("path", True).get_content()
        self.load_button = self.menu.root.find_node("LoadButton", True).get_content()
        self.save_button = self.menu.root.find_node("SaveButton", True).get_content()
        self.selected_button = None
        self.fetch_children()
        self.fetch_wd()
        self.temp_dir = tempfile.mkdtemp()
        self.load_count = 0

    def run(self):
        self.running = True
        self.update_menu(self.menu)

    def fetch_wd(self):
        self.wd = "."
        self.files.pwd(self.__set_dir)

    def __set_dir(self, error, wd):
        self.wd = wd
        self.path_text.text = wd
        if self.running:
            self.update_content(self.path_text)

    def fetch_children(self):
        self.files.ls(".", self.__set_children)

    def __set_children(self, error, files):
        if error != nanome.util.FileError.no_error: # If API couldn't access directory, display error
            nanome.util.Logs.error("Directory request error:", str(error))
            return
        self.grid.items = []
        for file in files:
            item = self.create_file_rep(file)
            self.grid.items.append(item)
        if self.running:
            self.update_content(self.grid)

    def create_file_rep(self, entry):
        item = self.item_prefab.clone()
        button = item.find_node("Button", True).get_content()
        button.register_pressed_callback(self.entry_pressed)
        button.entry = entry
        button.text.value.set_all(entry.name)
        return item

    def entry_pressed(self, button):
        to_update = []
        button.selected = True
        if self.selected_button is not None:
            self.selected_button.selected = False
            to_update.append(self.selected_button)
        if self.selected_button == button:
            self.selected_button = None
        else:
            self.selected_button = button
            to_update.append(self.selected_button)

        self.save_button.unusable = self.selected_button == None
        to_update.append(self.save_button)
        self.load_button.unusable = self.selected_button == None
        to_update.append(self.load_button)
        self.update_content(to_update)

    def load_pressed(self, button):
        entry = self.selected_button.entry
        if entry.is_directory:
            self.files.cd(entry.name, self.directory_changed)
        else:
            self.files.get(entry.name, os.path.join(self.temp_dir, str(self.load_count)), self.file_fetched)
            self.load_count+=1

    def file_fetched(self, error, path):
        if error != nanome.util.FileError.no_error:
            self.send_files_to_load(path)

    def save_pressed(self, button):
        pass

    def back_pressed(self, button):
        self.files.cd("..", self.directory_changed)

    def directory_changed(self, *args):
        self.fetch_wd()
        self.fetch_children()

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, FileExplorer)