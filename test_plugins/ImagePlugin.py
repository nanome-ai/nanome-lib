import nanome
import os
import sys

# Config

NAME = "Image Plugin"
DESCRIPTION = "Image Plugin."
CATEGORY = "Test"
HAS_ADVANCED_OPTIONS = False
NTS_ADDRESS = '127.0.0.1'
NTS_PORT = 8888

# Plugin

class ImagePlugin(nanome.PluginInstance):
    def __init__(self):
        pass
    # Function called when Nanome connects to the Plugin, after its instantiation
    def start(self):
        self.create_image_menu()
    # Function called when user clicks on the "Run" button in Nanome
    def on_run(self):
        self.open_menu()

    def on_advanced_settings(self):
        self.open_menu()

    def open_menu(self):
        self.menu.enabled = True
        self.update_menu(self.menu)

    def create_image_menu(self):
        self.menu = nanome.ui.Menu.io.from_json("ImageMenu.json")
        root = self.menu.root
        image_node = root.find_node("ImageNode")
        self.image = image_node.add_new_image(os.path.expanduser("~/Desktop/png.png"))
                
        width_node = root.find_node("WidthNode")
        height_node = root.find_node("HeightNode")

        fill_node = root.find_node("FillNode")
        fill_button = fill_node.add_new_button("fill")
        fill_button.name = "fill"
        fit_node = root.find_node("FitNode")
        fit_button = fit_node.add_new_button("fit")
        fit_button.name = "fit"
        stretch_node = root.find_node("StretchNode")
        stretch_button = stretch_node.add_new_button("stretch")
        stretch_button.name = "stretch"

        def image_pressed(image, x, y):
            print("image pressed (" + str(x) + ", " + str(y) + ")")

        def image_held(image, x, y):
            print("image held (" + str(x) + ", " + str(y) + ")")

        def image_released(image, x, y):
            print("image released (" + str(x) + ", " + str(y) + ")")

        def image_setting(button):
            name = button.name
            if (name == "fill"):
                self.image.scaling_option = nanome.util.enums.ScalingOptions.fill
            if (name == "fit"):
                self.image.scaling_option = nanome.util.enums.ScalingOptions.fit
            if (name == "stretch"):
                self.image.scaling_option = nanome.util.enums.ScalingOptions.stretch
            self.update_content(self.image)

        def setWidth(text_input):
            text = text_input.input_text
            width = 1.0
            try:
                width = float(text)
            except:
                width = 1.0
            self.menu.width = width
            self.update_menu(self.menu)

        def setHeight(text_input):
            text = text_input.input_text
            height = 1.0
            try:
                height = float(text)
            except:
                height = 1.0
            self.menu.height = height
            self.update_menu(self.menu)

        width = width_node.add_new_text_input()
        width.register_submitted_callback(setWidth)
        height = height_node.add_new_text_input()
        height.register_submitted_callback(setHeight)
        
        fill_button.register_pressed_callback(image_setting)
        fit_button.register_pressed_callback(image_setting)
        stretch_button.register_pressed_callback(image_setting)

        self.image.register_pressed_callback(image_pressed)
        self.image.register_released_callback(image_released)
        self.image.register_held_callback(image_held)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, ImagePlugin, NTS_ADDRESS, NTS_PORT)