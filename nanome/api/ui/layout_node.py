from nanome._internal._ui import _LayoutNode
from nanome.api.ui import Button, Slider, UIList, Mesh, Label, TextInput, Image, LoadingBar
class LayoutNode(_LayoutNode):
    def __init__(self, name = "node"):
        # type: (str)
        _LayoutNode.__init__(self, name)

    def clone(self):
        return self._clone()

    #region properties.
    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def name(self):
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
        return self._layer
    
    @layer.setter
    def layer(self, value):
        self._layer = value
        self._save_changes()

    @property
    def layout_orientation(self):
        return self._layout_orientation
    
    @layout_orientation.setter
    def layout_orientation(self, value):
        self._layout_orientation = value
        self._save_changes()

    @property
    def sizing_type(self):
        return self._sizing_type
    
    @sizing_type.setter
    def sizing_type(self, value):
        self._sizing_type = value
        self._save_changes()

    @property
    def sizing_value(self):
        return self._sizing_value
    
    @sizing_value.setter
    def sizing_value(self, value):
        self._sizing_value = value
        self._save_changes()

    @property
    def forward_dist(self):
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
    #region API Essentials
    def find_content(self, name, recursively = False):
        # type: (str, bool) -> UIBase
        """
        | Checks child nodes for an attached content of the matching name.
        | If "recursively" is True, this also checks all descending nodes' contents.

        :param name: Name of the content to find.
        :type name: str
        :return: Content with matching name.
        :rtype: :class:`~nanome.api.ui.ui_base.UIBase`
        """
        for content in self.get_content():
            if name == content.name:
                return content
        if recursively:
            for child in self.get_children():
                res = child.find_content(name, True)
                if res != None:
                    return res
        return None

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
        
    #endregion
    #region API Shortcuts

    def find_ancestor(self, name):
        if (self._parent != None):
            if (self._parent.name == name):
                return self._parent
            return self._parent.find_ancestor(name)
        return None

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
    def add_new_button(self, name = "button", text = None):
        # type: (str, str) -> Button
        button = Button(name=name, text=text)
        self.add_content(button)
        return button

    def add_new_label(self, name = "label", text = None):
        # type: (str, str) -> Label
        label = Label(name=name, text=text)
        self.add_content(label)
        return label

    def add_new_text_input(self, name = "text input"):
        # type: (str) -> TextInput
        text_input = TextInput(name=name)
        self.add_content(text_input)
        return text_input

    def add_new_slider(self, name = "slider"):
        # type: (str) -> Slider
        slider = Slider(name=name)
        self.add_content(slider)
        return slider

    def add_new_mesh(self, name = "mesh"):
        # type: (str) -> Mesh
        mesh = Mesh(name=name)
        self.add_content(mesh)
        return mesh

    def add_new_image(self, name = "image"):
        image = Image(name=name)
        self.add_content(image)
        return image

    def add_new_loading_bar(self):
        loadingBar = LoadingBar()
        self.add_content(loadingBar)
        return loadingBar

    def add_new_list(self, name = "list"):
        # type: (str) -> UIList
        list_ = UIList(name=name)
        self.add_content(list_)
        return list_
    #endregion
_LayoutNode._create = LayoutNode
