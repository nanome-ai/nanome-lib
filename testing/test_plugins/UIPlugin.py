import nanome
from nanome.util import Logs

# Config

NAME = "UI Plugin"
DESCRIPTION = "A simple plugin demonstrating how plugin system can be used to extend Nanome capabilities"
CATEGORY = "File Import"
HAS_ADVANCED_OPTIONS = False

# Plugin


def menu_closed_callback(menu):
    Logs.message("Menu closed: " + menu.title + " " + str(menu.enabled))


def menu_opened_callback(menu):
    Logs.message("Menu opened: " + menu.title + " " + str(menu.enabled))


def slider_changed_callback(slider):
    Logs.message("slider changed: " + str(slider.current_value))


def dropdown_callback(dropdown, item):
    Logs.message("dropdown item selected: " + str(item.name))


def slider_released_callback(slider):
    Logs.message("slider released: " + str(slider.current_value))


def text_changed_callback(textInput):
    Logs.message("text input changed: " + str(textInput.input_text))


def text_submitted_callback(textInput):
    Logs.message("text input submitted: " + str(textInput.input_text))


class UIPlugin(nanome.PluginInstance):

    def create_callbacks(self):
        def spawn_menu_callback(button):
            Logs.message("button pressed: " + button.text.value.idle)
            self.update_content(button)
            self.spawn_sub_menu()

        self.spawn_menu_callback = spawn_menu_callback

        def hover_callback(button, hovered):
            Logs.message("button hover: " + button.text.value.idle, hovered)

        self.hover_callback = hover_callback

        def select_button_callback(button):
            button.selected = not button.selected
            Logs.message("Prefab button pressed: " + button.text.value.idle + " " + str(button._content_id))
            self.update_content(button)

        self.select_button_callback = select_button_callback

        def loading_bar_callback(button):
            Logs.message("button pressed: " + button.text.value.idle)

            self.loadingBar.percentage += .1
            self.loadingBar.title = "TITLE"
            self.loadingBar.description = "DESCRIPTION " + str(self.loadingBar.percentage)

            self.update_content(self.loadingBar)

        self.loading_bar_callback = loading_bar_callback

    def start(self):
        self.integration.import_file = self.import_file
        Logs.message("Start UI Plugin")
        self.create_callbacks()

    def import_file(self, request):
        self.on_run()

    def on_run(self):
        Logs.message("Run UI Plugin")
        menu = self.rebuild_menu()
        self.update_menu(menu)

    def rebuild_menu(self):
        self.menu = nanome.ui.Menu()
        menu = self.menu
        menu.title = "Example UI Plugin"
        menu.width = 1.0
        menu.height = 1.0
        menu.register_closed_callback(menu_closed_callback)
        self.tab1 = self.create_tab1()
        self.tab2 = self.create_tab2()
        self.tab2.enabled = False
        self.tab_buttons = self.create_tab_buttons()
        menu.root.add_child(self.tab_buttons)
        self.tabs = menu.root.create_child_node()
        self.tabs.add_child(self.tab1)
        self.tabs.add_child(self.tab2)
        return menu

    def spawn_sub_menu(self):
        menu = nanome.api.ui.Menu(self.menu_index, "Menu " + str(self.menu_index))
        menu.register_closed_callback(menu_closed_callback)
        menu.width = 0.5
        menu.height = 0.5
        if self.previous_menu != None:
            ln = self.previous_menu.root.create_child_node()
            ln.add_new_label(str(self.menu_index - 1))
            self.update_menu(self.previous_menu)

        def change_title(button):
            menu.title = "New Title"
            self.update_menu(menu, True)

        root = menu.root
        button_node = root.create_child_node("button_node")
        button = button_node.add_new_button("button")
        button.register_pressed_callback(change_title)

        self.update_menu(menu)
        self.menu_index += 1
        self.previous_menu = menu

    def create_tab1(self):
        self.menu_index = 1
        self.previous_menu = None

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

        Logs.message("Added Label")

        ln_button.padding_type = nanome.ui.LayoutNode.PaddingTypes.ratio
        ln_button.padding = (0.01, 0.01, 0.01, 0.01)
        ln_button.forward_dist = .001

        # super styled button
        button = nanome.ui.Button()
        button.name = "OpenSubMenu"
        b_t = button.text
        b_t.active = True
        b_t.value.set_all("Spawn menu")
        b_t.auto_size = False
        b_t.size = .6
        b_t.underlined = True
        b_t.ellipsis = True
        b_t.color.idle = nanome.util.Color.Red()
        b_t.color.highlighted = nanome.util.Color.Blue()
        b_t.bold.set_all(False)
        b_t.padding_left = .5
        b_t.vertical_align = nanome.util.enums.VertAlignOptions.Middle
        b_t.horizontal_align = nanome.util.enums.HorizAlignOptions.Left
        b_m = button.mesh
        b_m.active = True
        b_m.color.idle = nanome.util.Color.Blue()
        b_m.color.highlighted = nanome.util.Color.Red()
        b_o = button.outline
        b_o.active = True
        b_o.color.idle = nanome.util.Color.Red()
        b_o.color.highlighted = nanome.util.Color.Blue()
        b_t = button.tooltip
        b_t.title = "spawn a submenu"
        b_t.content = "it is useless"
        b_t.positioning_target = nanome.util.enums.ToolTipPositioning.center
        button.register_pressed_callback(self.spawn_menu_callback)
        button.register_hover_callback(self.hover_callback)

        Logs.message("Added button")

        ln_slider.padding_type = nanome.ui.LayoutNode.PaddingTypes.ratio
        ln_slider.padding = (0.01, 0.01, 0.01, 0.01)
        ln_slider.forward_dist = .001

        slider = nanome.ui.Slider()
        slider.register_changed_callback(slider_changed_callback)
        slider.register_released_callback(slider_released_callback)

        Logs.message("Added slider")

        ln_textInput.padding_type = nanome.ui.LayoutNode.PaddingTypes.ratio
        ln_textInput.padding = (0.01, 0.01, 0.01, 0.01)
        ln_textInput.forward_dist = .001

        textInput = nanome.ui.TextInput()
        textInput.max_length = 30
        textInput.register_changed_callback(text_changed_callback)
        textInput.register_submitted_callback(text_submitted_callback)
        textInput.number = True
        textInput.text_color = nanome.util.Color.Blue()
        textInput.placeholder_text_color = nanome.util.Color.Red()
        textInput.background_color = nanome.util.Color.Grey()
        textInput.text_horizontal_align = nanome.ui.TextInput.HorizAlignOptions.Right
        textInput.padding_right = .2
        textInput.text_size = .6

        Logs.message("Added text input")

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
        child2.forward_dist = .01
        prefab.add_child(child1)
        prefab.add_child(child2)
        prefabLabel = nanome.ui.Label()
        prefabLabel.text_value = "Molecule Label"
        prefabButton = nanome.ui.Button()
        prefabButton.text.active = True
        prefabButton.text.value.set_all("Molecule Button")
        prefabButton.disable_on_press = True
        prefabButton.register_pressed_callback(self.select_button_callback)
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

        Logs.message("Added list")

        content.add_child(ln_contentBase)
        ln_contentBase.add_child(ln_label)
        ln_contentBase.add_child(ln_button)
        ln_contentBase.add_child(ln_slider)
        ln_contentBase.add_child(ln_textInput)
        ln_contentBase.add_child(ln_list)
        ln_label.set_content(label)
        ln_button.set_content(button)
        ln_slider.set_content(slider)
        ln_textInput.set_content(textInput)
        ln_list.set_content(list)
        return content

    def create_tab2(self):
        content = nanome.ui.LayoutNode()
        ln_contentBase = nanome.ui.LayoutNode()
        ln_label = nanome.ui.LayoutNode()
        ln_button = nanome.ui.LayoutNode()
        ln_dropdown = nanome.ui.LayoutNode()
        ln_textInput = nanome.ui.LayoutNode()

        content.forward_dist = .02
        content.layer = 1

        ln_label.padding_type = nanome.ui.LayoutNode.PaddingTypes.ratio
        ln_label.padding = (0.01, 0.01, 0.01, 0.01)
        ln_label.forward_dist = .001

        label = nanome.ui.Label()
        label.text_value = "Press the button..."
        label.text_color = nanome.util.Color.White()

        Logs.message("Added Label")

        ln_button.padding_type = nanome.ui.LayoutNode.PaddingTypes.ratio
        ln_button.padding = (0.01, 0.01, 0.01, 0.01)
        ln_button.forward_dist = .001

        button = ln_button.add_new_toggle_switch("Toggle Switch")
        button.text.size = .5
        button.text.auto_size = False
        button.register_pressed_callback(self.loading_bar_callback)
        button.register_hover_callback(self.hover_callback)

        Logs.message("Added button")

        ln_dropdown.padding_type = nanome.ui.LayoutNode.PaddingTypes.ratio
        ln_dropdown.padding = (0.01, 0.01, 0.01, 0.01)
        ln_dropdown.forward_dist = .004

        dropdown = nanome.ui.Dropdown()
        dropdown.items = [nanome.ui.DropdownItem(name) for name in ["option1", "option2", "option3", "option4", "option5", "option6"]]
        dropdown.register_item_clicked_callback(dropdown_callback)

        Logs.message("Added dropdown")

        ln_textInput.padding_type = nanome.ui.LayoutNode.PaddingTypes.ratio
        ln_textInput.padding = (0.01, 0.01, 0.01, 0.01)
        ln_textInput.forward_dist = .001

        textInput = nanome.ui.TextInput()
        textInput.max_length = 30
        textInput.register_changed_callback(text_changed_callback)
        textInput.register_submitted_callback(text_submitted_callback)
        textInput.password = True
        textInput.input_text = "hello"

        Logs.message("Added text input")

        prefab = nanome.ui.LayoutNode()
        prefab.layout_orientation = nanome.ui.LayoutNode.LayoutTypes.vertical
        child1 = nanome.ui.LayoutNode()
        child1.sizing_type = nanome.ui.LayoutNode.SizingTypes.ratio
        child1.sizing_value = .3
        child1.name = "label"
        child1.forward_dist = .01
        child2 = nanome.ui.LayoutNode()
        child2.name = "button"
        child2.forward_dist = .01
        prefab.add_child(child1)
        prefab.add_child(child2)
        prefabLabel = nanome.ui.Label()
        prefabLabel.text_value = "Molecule Label"
        prefabButton = nanome.ui.Button()
        prefabButton.text.active = True
        prefabButton.text.value.set_all("Molecule Button")
        prefabButton.register_pressed_callback(self.select_button_callback)
        child1.set_content(prefabLabel)
        child2.set_content(prefabButton)

        ln_loading_bar = nanome.ui.LayoutNode(name="LoadingBar")
        ln_loading_bar.forward_dist = .003
        self.loadingBar = ln_loading_bar.add_new_loading_bar()

        content.add_child(ln_contentBase)
        ln_contentBase.add_child(ln_label)
        ln_contentBase.add_child(ln_button)
        ln_contentBase.add_child(ln_dropdown)
        ln_contentBase.add_child(ln_textInput)
        ln_contentBase.add_child(ln_loading_bar)
        ln_label.set_content(label)
        ln_button.set_content(button)
        ln_dropdown.set_content(dropdown)
        ln_textInput.set_content(textInput)
        return content

    def create_tab_buttons(self):
        LN = nanome.ui.LayoutNode
        ln = LN()
        ln.layout_orientation = nanome.util.enums.LayoutTypes.horizontal
        ln._sizing_type = nanome.util.enums.SizingTypes.fixed
        ln._sizing_value = .1

        def tab1_callback(button):
            self.tab_button1.selected = True
            self.tab_button2.selected = False
            self.tab1.enabled = True
            self.tab2.enabled = False

            self.update_node(self.tabs)
            self.update_content(self.tab_button1, self.tab_button2)

        def tab2_callback(button):
            self.tab_button2.selected = True
            self.tab_button1.selected = False
            self.tab2.enabled = True
            self.tab1.enabled = False

            self.update_node(self.tabs)
            self.update_content([self.tab_button2, self.tab_button1])

        tab_button_node1 = ln.create_child_node("tab1")
        self.tab_button1 = tab_button_node1.add_new_button("tab1")
        self.tab_button1.register_pressed_callback(tab1_callback)
        tab_button_node2 = ln.create_child_node("tab2")
        self.tab_button2 = tab_button_node2.add_new_button("tab2")
        self.tab_button2.register_pressed_callback(tab2_callback)
        return ln


permissions = [nanome.util.enums.Permissions.local_files_access]
integrations = [nanome.util.enums.Integrations.minimization, nanome.util.enums.Integrations.structure_prep]

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, UIPlugin, permissions=permissions, integrations=integrations)
