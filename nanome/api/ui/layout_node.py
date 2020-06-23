import nanome
from nanome._internal._ui import _LayoutNode
from nanome.api.ui import Button, Slider, UIList, Mesh, Label, TextInput, Image, LoadingBar, Dropdown
from .io import LayoutNodeIO

class LayoutNode(_LayoutNode):
    """
    | Class containing UI elements. Layout nodes are used to architecture menus, by defining where one UI element should be placed relatively to another.
    | One layout node can contain one UI element, and several children Layout Nodes.

    :param name: Name of the node, used to identify it and find it later
    :type name: :class:`str`
    """
    PaddingTypes = nanome.util.enums.PaddingTypes
    SizingTypes = nanome.util.enums.SizingTypes
    LayoutTypes = nanome.util.enums.LayoutTypes

    io = LayoutNodeIO()
    def __init__(self, name = "node"):
        _LayoutNode.__init__(self, name)
        self.io = LayoutNodeIO(self)

    def clone(self):
        return self._clone()

    #region properties.
    @property
    def enabled(self):
        """
        | Defines if layout node is visible.
        | If disabled, it will not influence the menu layout.

        :type: :class:`bool`
        """
        return self._enabled
    
    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def name(self):
        """
        | Name of the node, used to identify it and find it later

        :type: :class:`str`
        """
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def padding_type(self):
        return self._padding_type
    
    @padding_type.setter
    def padding_type(self, value):
        self._padding_type = value
        self._save_changes()

    @property
    def layer(self):
        """
        | The node layer. A node on layer 0 and another on layer 1 will be on different layouts, possibly overlapping

        :type: :class:`int`
        """
        return self._layer
    
    @layer.setter
    def layer(self, value):
        self._layer = value
        self._save_changes()

    @property
    def layout_orientation(self):
        """
        | Defines if children node should be arranged vertically or horizontally

        :type: :class:`~LayoutOrientation`
        """
        return self._layout_orientation
    
    @layout_orientation.setter
    def layout_orientation(self, value):
        self._layout_orientation = value
        self._save_changes()

    @property
    def sizing_type(self):
        """
        | Defines how the node size in the layout should be calculated

        :type: :class:`~SizingTypes`
        """
        return self._sizing_type
    
    @sizing_type.setter
    def sizing_type(self, value):
        self._sizing_type = value
        self._save_changes()

    @property
    def sizing_value(self):
        """
        | Size of the node in its layout.
        | Behavior is different depending of :attr:`~sizing_type`

        :type: :class:`float`
        """
        return self._sizing_value
    
    @sizing_value.setter
    def sizing_value(self, value):
        self._sizing_value = value
        self._save_changes()

    @property
    def forward_dist(self):
        """
        | Sets the depth distance (towards camera) of a node, relative to its parent

        :type: :class:`float`
        """
        return self._forward_dist
    
    @forward_dist.setter
    def forward_dist(self, value):
        self._forward_dist = value
        self._save_changes()

    @property
    def padding(self):
        return self._padding
    
    @padding.setter
    def padding(self, value):
        self._padding = value
        self._save_changes()

    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value):
        self._parent = value
    #endregion
    #region API functions
    def find_node(self, name, recursively = True):
        # type: (str, bool) -> LayoutNode
        """
        | Checks child nodes for a node of the matching name.
        | If "recursively" is True, this also checks all descending nodes.

        :param name: Name of the node to find.
        :type name: str
        :return: LayoutNode with matching name
        :rtype: :class:`~nanome.api.ui.layout_node.LayoutNode`
        """
        res = None
        for child in self.get_children():
            if name == child.name:
                res = child
            elif recursively:
                res = child.find_node(name, True)
            if res != None:
                break
        return res
        
    def find_ancestor(self, name):
        if (self._parent != None):
            if (self._parent.name == name):
                return self._parent
            return self._parent.find_ancestor(name)
        return None

    def get_children(self):
        return self._get_children()

    def get_content(self):
        return self._get_content()

    def set_content(self, ui_content):
        self._set_content(ui_content)

    def remove_content(self):
        self._remove_content()

    def add_child(self, child_node):
        self._add_child(child_node)

    def remove_child(self, child_node):
        self._remove_child(child_node)

    def clear_children(self):
        self._clear_children()

    #endregion
    #region API Shortcuts

    def create_child_node(self, name = ""):
        child = LayoutNode(name)
        self.add_child(child)
        return child

    def set_padding(self, left=None, right=None, top=None, down=None):
        self.padding = (
            left if left != None else self.padding[0],
            right if right != None else self.padding[1],
            top if top != None else self.padding[2],
            down if down != None else self.padding[3]
        )

    def set_size_ratio(self, size):
        self.sizing_type = _LayoutNode.SizingTypes.ratio
        self.sizing_value = size

    def set_size_fixed(self, size):
        self.sizing_type = _LayoutNode.SizingTypes.fixed
        self.sizing_value = size

    def set_size_expand(self):
        self.sizing_type = _LayoutNode.SizingTypes.expand
    #endregion
    #region Content adders
    def add_new_button(self, text = None):
        # type: (str) -> Button
        button = Button(text=text)
        self.set_content(button)
        return button

    def add_new_label(self, text = None):
        # type: (str) -> Label
        label = Label(text=text)
        self.set_content(label)
        return label

    def add_new_text_input(self):
        # type: () -> TextInput
        text_input = TextInput()
        self.set_content(text_input)
        return text_input

    def add_new_slider(self, min_value = 0, max_value = 10, current_value = 5):
        # type: () -> Slider
        slider = Slider(min_value, max_value, current_value)
        self.set_content(slider)
        return slider

    def add_new_mesh(self):
        # type: () -> Mesh
        mesh = Mesh()
        self.set_content(mesh)
        return mesh

    def add_new_image(self, file_path = ""):
        image = Image(file_path)
        self.set_content(image)
        return image

    def add_new_loading_bar(self):
        loadingBar = LoadingBar()
        self.set_content(loadingBar)
        return loadingBar

    def add_new_list(self):
        # type: () -> UIList
        list_ = UIList()
        self.set_content(list_)
        return list_

    def add_new_dropdown(self):
        # type: () -> Dropdown
        dropdown_ = Dropdown()
        self.set_content(dropdown_)
        return dropdown_
    #endregion
LayoutNode.io._setup_addon(LayoutNode)
_LayoutNode._create = LayoutNode