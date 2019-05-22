from nanome._internal._ui import _LayoutNode
from nanome.api.ui import Button, Slider, UIList, Mesh, Label, TextInput, Image, LoadingBar
from .io import LayoutNodeIO

class LayoutNode(_LayoutNode):
    io = LayoutNodeIO()
    def __init__(self, name = "node"):
        # type: (str)
        _LayoutNode.__init__(self, name)
        self.io = LayoutNodeIO(self)

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
    def add_new_button(self, text = None):
        # type: (str, str) -> Button
        button = Button(text=text)
        self.set_content(button)
        return button

    def add_new_label(self, text = None):
        # type: (str, str) -> Label
        label = Label(text=text)
        self.set_content(label)
        return label

    def add_new_text_input(self):
        # type: (str) -> TextInput
        text_input = TextInput()
        self.set_content(text_input)
        return text_input

    def add_new_slider(self, min_value = 0, max_value = 10, current_value = 5):
        # type: (str) -> Slider
        slider = Slider(min_value, max_value, current_value)
        self.set_content(slider)
        return slider

    def add_new_mesh(self):
        # type: (str) -> Mesh
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
        # type: (str) -> UIList
        list_ = UIList()
        self.set_content(list_)
        return list_
    #endregion
LayoutNode.io._setup_addon(LayoutNode)
_LayoutNode._create = LayoutNode