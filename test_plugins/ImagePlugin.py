import nanome
import os
import sys

class ImagePlugin(nanome.PluginInstance):
    def __init__(self):
        pass
    # Function called when Nanome connects to the Plugin, after its instantiation
    def start(self):
        self.menu = nanome.ui.Menu.get_plugin_menu()
        content = self.menu.root.create_child_node()
        image = content.add_new_image()
        image.file_path = os.path.expanduser("~/Desktop/png.png")

    # Function called when user clicks on the "Run" button in Nanome
    def on_run(self):
        self.open_menu()

    def on_advanced_settings(self):
        self.open_menu()

    def open_menu(self):
        menu = nanome.ui.Menu.get_plugin_menu()
        menu.enabled = True
        self.update_menu(menu)

if __name__ == "__main__":
    # Create the plugin, register Docking as the class to instantiate, and start listening
    plugin = nanome.Plugin("Image Plugin", "Image Plugin.", "Test", False)
    plugin.set_plugin_class(ImagePlugin)
    plugin.run('127.0.0.1', 8888)