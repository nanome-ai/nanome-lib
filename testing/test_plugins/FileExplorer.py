import os
import tempfile
import ntpath

import nanome
from nanome.api.ui import Menu, LayoutNode
from nanome.util import async_callback, Logs

NAME = "File Explorer"
DESCRIPTION = "Allows you to browse your files"
CATEGORY = ""
HAS_ADVANCED_OPTIONS = False

test_assets = os.getcwd() + ("/testing/test_assets")


class FileExplorer(nanome.AsyncPluginInstance):

    def start(self):
        self.running = False
        self.item_prefab = LayoutNode.io.from_json(test_assets + "/File.json")
        self.menu = Menu.io.from_json(test_assets + "/FileExplorer.json")
        self.grid = self.menu.root.find_node("Grid", True).get_content()
        self.path_text = self.menu.root.find_node("path", True).get_content()
        self.load_button = self.menu.root.find_node("LoadButton", True).get_content()
        self.load_button.register_pressed_callback(self.load_pressed)
        self.save_button = self.menu.root.find_node("SaveButton", True).get_content()
        self.save_button.register_pressed_callback(self.save_pressed)
        self.back_button = self.menu.root.find_node("back", True).get_content()
        self.back_button.register_pressed_callback(self.back_pressed)
        self.selected_button = None
        self.fetch_path()
        self.temp_dir = tempfile.mkdtemp()
        # self.test_path = "C:\\Users\\ETHANV~1\\AppData\\Local\\Temp\\tmpuzepx_cf\\file.jpg"
        # self.test_path1 = "C:\\Users\\ETHANV~1\\AppData\\Local\\Temp\\tmpuzepx_cf\\1.jpg"
        # self.test_path2 = "C:\\Users\\ETHANV~1\\AppData\\Local\\Temp\\tmpuzepx_cf\\2.jpg"
        # self.test_path3 = "C:\\Users\\ETHANV~1\\AppData\\Local\\Temp\\tmpuzepx_cf\\3.jpg"
        # self.files.cp(self.test_path, self.test_path1, self.cp_done)
        # self.files.put(self.test_path, self.test_path2, self.put_done)
        # self.files.mv(self.test_path, self.test_path3, self.mv_done)

    # def cp_done(self, *args):
    #     Logs.debug("cp done")

    # def put_done(self, *args):
    #     Logs.debug("put done")

    # def mv_done(self, *args):
    #     Logs.debug("mv done")

    def on_run(self):
        self.running = True
        self.update_menu(self.menu)

    @async_callback
    async def fetch_path(self, *_):
        error, wd = await self.files.pwd()
        self.path_text.text_value = wd
        if self.running:
            self.update_content(self.path_text)

        error, files = await self.files.ls(".")
        if error != nanome.util.FileError.no_error:  # If API couldn't access directory, display error
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
        button.text.value.set_all(entry.name)
        button.register_pressed_callback(self.entry_pressed)
        button.entry = entry
        button.text.value.set_all(self.path_leaf(entry.name))
        button.text.size = .3
        button.text.ellipsis = True
        return item

    def entry_pressed(self, button):
        if button.entry.is_directory:
            self.files.cd(button.entry.name, self.fetch_path)
            return
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

    @async_callback
    async def load_pressed(self, button):
        entry = self.selected_button.entry
        if entry.is_directory:
            return

        dest = os.path.join(self.temp_dir, str(self.path_leaf(entry.name)))
        error, path = await self.files.get(entry.name, dest)
        if error == nanome.util.FileError.no_error:
            Logs.debug(path)
            self.send_files_to_load(path)
        else:
            Logs.debug(error)

    def save_pressed(self, button):
        pass

    def back_pressed(self, button):
        self.files.cd("..", self.fetch_path)

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, FileExplorer, permissions=[nanome.util.enums.Permissions.local_files_access])
