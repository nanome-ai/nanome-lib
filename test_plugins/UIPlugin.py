import nanome
from nanome.util import Logs
import sys
import time

# Config

NAME = "UI Plugin"
DESCRIPTION = "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities"
CATEGORY = "Simple Actions"
HAS_ADVANCED_OPTIONS = False
NTS_ADDRESS = '127.0.0.1'
NTS_PORT = 8888

# Plugin

def menu_closed_callback(menu): 
    Logs.debug("Menu closed: " + menu.title + " " + str(menu.enabled))

def menu_opened_callback(menu): 
    Logs.debug("Menu opened: " + menu.title + " " + str(menu.enabled))

def slider_changed_callback(slider): 
    Logs.debug("slider changed: " + str(slider.current_value))

def slider_released_callback(slider): 
    Logs.debug("slider released: " + str(slider.current_value))

def text_changed_callback(textInput): 
    Logs.debug("text input changed: " + str(textInput.input_text))

def text_submitted_callback(textInput): 
    Logs.debug("text input submitted: " + str(textInput.input_text))

class UIPlugin(nanome.PluginInstance):
    inited = False

    def init(self):
        self.menu = self.rebuild_menu()

    def start(self):
        Logs.debug("Start UI Plugin")
    
    def on_run(self):
        Logs.debug("Run UI Plugin")
        menu = self.rebuild_menu()
        self.update_menu(menu)

    def rebuild_menu(self):
        menu = self.menu
        menu.title = "Example UI Plugin"
        menu.width = 1.0
        menu.height =  1.0
        menu.register_closed_callback(menu_closed_callback)
        menu.register_opened_callback(menu_opened_callback)
        self.tab1 = self.create_tab1()
        self.tab2 = self.create_tab2()
        self.tab_buttons = self.create_tab_buttons()
        menu.root.add_child(self.tab_buttons)
        menu.root.add_child(self.tab1)
        menu.root.add_child(self.tab2)
        return menu

    def create_tab1(self):
        def button_pressed_callback(button): 
            Logs.debug("button pressed: " + button.text.value_idle)
            button.text.value_selected = "Button Pressed!"
            button.selected = not button.selected

            self.loadingBar.percentage += .1
            self.loadingBar.title = "TITLE"
            self.loadingBar.description = "DESCRIPTION " + str(self.loadingBar.percentage)

            self.update_content(button)
            self.update_content(self.loadingBar)

        def hover_callback(button, hovered): 
            Logs.debug("button hover: " + button.text.value_idle, hovered)

        def prefab_button_pressed_callback(button):
            button.selected = not button.selected
            Logs.debug("Prefab button pressed: " + button.text.value_idle + " " + str(button._content_id))
            self.update_content(button)
        
        content = nanome.ui.LayoutNode()
        ln_contentBase = nanome.ui.LayoutNode()
        ln_label = nanome.ui.LayoutNode()
        ln_button = nanome.ui.LayoutNode()
        ln_slider = nanome.ui.LayoutNode()
        ln_textInput = nanome.ui.LayoutNode()
        ln_list = nanome.ui.LayoutNode()

        content.forward_dist = .02
        content.layer = 1

        ln_label.padding_type = nanome.ui.LayoutNode.PaddingTypes.ratio
        ln_label.padding = (0.01, 0.01, 0.01, 0.01)
        ln_label.forward_dist = .001

        label = nanome.ui.Label()
        label.text_value = "Press the button..."
        label.text_color = nanome.util.Color.White()

        Logs.debug("Added Label")

        ln_button.padding_type = nanome.ui.LayoutNode.PaddingTypes.ratio
        ln_button.padding = (0.01, 0.01, 0.01, 0.01)
        ln_button.forward_dist = .001

        button = nanome.ui.Button()
        button.text.active = True
        button.text.vertical_align = nanome.util.enums.VertAlignOptions.Middle
        button.text.horizontal_align = nanome.util.enums.HorizAlignOptions.Middle
        button.register_pressed_callback(button_pressed_callback)
        button.register_hover_callback(hover_callback)

        Logs.debug("Added button")

        ln_slider.padding_type = nanome.ui.LayoutNode.PaddingTypes.ratio
        ln_slider.padding = (0.01, 0.01, 0.01, 0.01)
        ln_slider.forward_dist = .001

        slider = nanome.ui.Slider()
        slider.register_changed_callback(slider_changed_callback)
        slider.register_released_callback(slider_released_callback)

        Logs.debug("Added slider")

        ln_textInput.padding_type = nanome.ui.LayoutNode.PaddingTypes.ratio
        ln_textInput.padding = (0.01, 0.01, 0.01, 0.01)
        ln_textInput.forward_dist = .001

        textInput = nanome.ui.TextInput()
        textInput.max_length = 30
        textInput.register_changed_callback(text_changed_callback)
        textInput.register_submitted_callback(text_submitted_callback)

        Logs.debug("Added text input")

        ln_list.sizing_type = nanome.ui.LayoutNode.SizingTypes.ratio
        ln_list.sizing_value = 0.5
        ln_list.padding_type = nanome.ui.LayoutNode.PaddingTypes.ratio
        ln_list.padding = (0.01, 0.01, 0.01, 0.01)
        ln_list.forward_dist = .03

        prefab = nanome.ui.LayoutNode()
        prefab.layout_orientation = nanome.ui.LayoutNode.LayoutTypes.vertical
        child1 = nanome.ui.LayoutNode()
        child1.sizing_type = nanome.ui.LayoutNode.SizingTypes.ratio
        child1.sizing_value = .3
        child1.name = "label"
        child1.forward_dist = .01
        child2 = nanome.ui.LayoutNode()
        child2.name = "button"
        child2.forward_dist =.01
        prefab.add_child(child1)
        prefab.add_child(child2)
        prefabLabel = nanome.ui.Label()
        prefabLabel.text_value = "Molecule Label"
        prefabButton = nanome.ui.Button()
        prefabButton.text.active = True
        prefabButton.set_all_text("Molecule Button")
        prefabButton.register_pressed_callback(prefab_button_pressed_callback)
        child1.set_content(prefabLabel)
        child2.set_content(prefabButton)

        list_content = []
        for i in range(0, 10):
            clone = prefab.clone()
            list_content.append(clone)

        list = nanome.ui.UIList()
        list.display_columns = 1
        list.display_rows = 1
        list.total_columns = 1
        list.items = list_content

        Logs.debug("Added list")

        ln_loading_bar = nanome.ui.LayoutNode(name="LoadingBar")
        ln_loading_bar.forward_dist = .03
        self.loadingBar = ln_loading_bar.add_new_loading_bar()

        content.add_child(ln_contentBase)
        ln_contentBase.add_child(ln_label)
        ln_contentBase.add_child(ln_button)
        ln_contentBase.add_child(ln_slider)
        ln_contentBase.add_child(ln_textInput)
        ln_contentBase.add_child(ln_list) 
        ln_contentBase.add_child(ln_loading_bar)
        ln_label.set_content(label)
        ln_button.set_content(button)
        ln_slider.set_content(slider)
        ln_textInput.set_content(textInput)
        ln_list.set_content(list)
        return content

    def create_tab2(self):
        pass

    def create_tab_buttons(self):
        LN = nanome.ui.LayoutNode
        ln = LN()
        tab_button_node1 = ln.create_child_node("tab1")
        tab_button_node1.add_new_button("tab1")
        tab_button_node2 = ln.create_child_node("tab2")
        tab_button_node2.add_new_button("tab2")


    def __init__(self):
        pass

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, UIPlugin)