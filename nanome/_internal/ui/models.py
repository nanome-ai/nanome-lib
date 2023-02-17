from copy import deepcopy
import logging

from nanome._internal import enums, network

logger = logging.getLogger(__name__)


class _UIBase(object):
    id_gen = 0

    def __init__(self):
        # protocol
        self._content_id = _UIBase.id_gen
        _UIBase.id_gen += 1

    def _copy_values_deep(self, other):
        pass

    def _clone(self):
        result = self.__class__()
        result._copy_values_deep(self)
        return result


class _Button(_UIBase):

    @property
    def HorizAlignOptions(self):
        from nanome.util import enums
        return enums.HorizAlignOptions

    @property
    def VertAlignOptions(self):
        from nanome.util import enums
        return enums.VertAlignOptions

    @property
    def ToolTipPositioning(self):
        from nanome.util import enums
        return enums.ToolTipPositioning

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Button, self).__init__()
        # PROTOCOL
        self._name = ""
        self._selected = False
        self._unusable = False
        self._disable_on_press = False
        self._toggle_on_press = False
        self._text = _Button._ButtonText._create()
        self._icon = _Button._ButtonIcon._create()
        self._mesh = _Button._ButtonMesh._create()
        self._outline = _Button._ButtonOutline._create()
        self._switch = _Button._ButtonSwitch._create()
        self._tooltip = _Button._ButtonTooltip._create()
        # API
        self._pressed_callback = lambda _: None
        self._hover_callback = None

    def _on_button_pressed(self):
        self._pressed_callback(self)

    def _on_button_hover(self, state):
        if self._hover_callback != None:
            self._hover_callback(self, state)

    def _register_pressed_callback(self, func):
        self._pressed_callback = func

    def _register_hover_callback(self, func):
        from nanome.api.ui import messages
        message_callbacks = enums.Messages
        if func == None and self._hover_callback == None:  # Low hanging filter but there may be others
            return
        try:
            network.PluginNetwork._instance.send(
                message_callbacks.hook_ui_callback,
                (messages.UIHook.Type.button_hover, self._content_id),
                False)
        except:
            logger.error("Could not register hook")
        self._hover_callback = func

    class _ButtonText(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            from nanome.util import Color, enums
            self._active = True
            self._value = _Button._MultiStateVariable._create("text")
            self._auto_size = True
            self._min_size = 0.0
            self._max_size = .3
            self._size = 0.2
            self._underlined = False
            self._ellipsis = True
            self._bold = _Button._MultiStateVariable._create(True)
            self._color = _Button._MultiStateVariable._create(Color.White())
            self._padding_top = 0.0
            self._padding_bottom = 0.0
            self._padding_left = 0.0
            self._padding_right = 0.0
            self._line_spacing = 0.0
            self._vertical_align = enums.VertAlignOptions.Middle
            self._horizontal_align = enums.HorizAlignOptions.Middle

    class _ButtonIcon(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            from nanome.util import Vector3, Color
            self._active = False
            self._value = _Button._MultiStateVariable._create("")
            self._color = _Button._MultiStateVariable._create(Color.White())
            self._sharpness = 0.5
            self._size = 1.0
            self._ratio = 0.5
            self._position = Vector3()
            self._rotation = Vector3()

    class _ButtonMesh(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            from nanome.util import Color
            self._active = False
            self._enabled = _Button._MultiStateVariable._create(True)
            self._color = _Button._MultiStateVariable._create(Color.Black())

    class _ButtonOutline(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            from nanome.util import Color
            self._active = True
            self._size = _Button._MultiStateVariable._create(.3)
            self._color = _Button._MultiStateVariable._create()
            self._color._idle = Color.White()
            self._color._highlighted = Color(whole_num=0x2fdbbfff)
            self._color._selected = Color(whole_num=0x00e5bfff)
            self._color._selected_highlighted = Color(whole_num=0x00f9d0ff)
            self._color._unusable = Color.Grey()

    class _ButtonSwitch(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            from nanome.util import Color
            self._active = False
            self._on_color = Color.from_int(0x00FFD5FF)
            self._off_color = Color.from_int(0x727272FF)

    class _ButtonTooltip(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            from nanome.util import Vector3, enums
            self._title = ""
            self._content = ""
            self._bounds = Vector3(1.73, .6, .05)
            self._positioning_target = enums.ToolTipPositioning.right
            self._positioning_origin = enums.ToolTipPositioning.top_left

    def _copy_values_deep(self, other):
        super(_Button, self)._copy_values_deep(other)
        # States
        self._name = other._name
        self._selected = other._selected
        self._unusable = other._unusable
        self._disable_on_press = other._disable_on_press
        self._toggle_on_press = other._toggle_on_press
        # Text
        self._text._active = other._text._active
        self._text._value._copy(other._text._value)
        self._text._auto_size = other._text._auto_size
        self._text._min_size = other._text._min_size
        self._text._max_size = other._text._max_size
        self._text._size = other._text._size
        self._text._underlined = other._text._underlined
        self._text._ellipsis = other._text._ellipsis
        self._text._bold._copy(other._text._bold)
        self._text._color._copy(other._text._color)
        self._text._padding_top = other._text._padding_top
        self._text._padding_bottom = other._text._padding_bottom
        self._text._padding_left = other._text._padding_left
        self._text._padding_right = other._text._padding_right
        self._text._line_spacing = other._text._line_spacing
        self._text._vertical_align = other._text._vertical_align
        self._text._horizontal_align = other._text._horizontal_align
        # Icon
        self._icon._active = other._icon._active
        self._icon._value._copy(other._icon._value)
        self._icon._color._copy(other._icon._color)
        self._icon._sharpness = other._icon._sharpness
        self._icon._size = other._icon._size
        self._icon._ratio = other._icon._ratio
        self._icon._position = other._icon._position
        self._icon._rotation = other._icon._rotation
        # Mesh
        self._mesh._active = other._mesh._active
        self._mesh._enabled._copy(other._mesh._enabled)
        self._mesh._color._copy(other._mesh._color)
        # Outline
        self._outline._active = other._outline._active
        self._outline._size._copy(other._outline._size)
        self._outline._color._copy(other._outline._color)
        # Tooltip
        self._tooltip._title = other._tooltip._title
        self._tooltip._content = other._tooltip._content
        self._tooltip._bounds = other._tooltip._bounds
        self._tooltip._positioning_target = other._tooltip._positioning_target
        self._tooltip._positioning_origin = other._tooltip._positioning_origin
        # Switch
        self._switch._active = other._switch._active
        self._switch._on_color = other._switch._on_color
        self._switch._off_color = other._switch._off_color
        # Callbacks
        self._pressed_callback = other._pressed_callback
        self._register_hover_callback(other._hover_callback)

    class _MultiStateVariable(object):
        @classmethod
        def _create(cls, default=None):
            return cls()

        def __init__(self, default=None):
            self._set_all(default)

        def _set_all(self, value):
            self._idle = deepcopy(value)
            self._highlighted = deepcopy(value)
            self._selected = deepcopy(value)
            self._selected_highlighted = deepcopy(value)
            self._unusable = deepcopy(value)

        def _set_each(self, idle=None, selected=None, highlighted=None, selected_highlighted=None, unusable=None, default=None):
            self._idle = deepcopy(idle) or deepcopy(default) or self._idle
            self._highlighted = deepcopy(highlighted) or deepcopy(
                default) or self._highlighted
            self._selected = deepcopy(selected) or deepcopy(
                default) or self._selected
            self._selected_highlighted = deepcopy(selected_highlighted) or deepcopy(
                selected) or deepcopy(default) or self._selected_highlighted
            self._unusable = deepcopy(unusable) or deepcopy(
                default) or self._unusable

        def _copy(self, other):
            self._idle = other._idle
            self._highlighted = other._highlighted
            self._selected = other._selected
            self._selected_highlighted = other._selected_highlighted
            self._unusable = other._unusable


class _Dropdown(_UIBase):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Dropdown, self).__init__()
        self._permanent_title = ""
        self._use_permanent_title = False
        self._max_displayed_items = 3
        self._unusable = False
        self._items = []
        self._item_clicked_callback = lambda self, item: None

    def _on_item_clicked(self, item):
        self._item_clicked_callback(self, item)

    def _register_item_clicked_callback(self, func):
        self._item_clicked_callback = func

    def _copy_values_deep(self, other):
        super(_Dropdown, self)._copy_values_deep(other)
        self._permanent_title = other._permanent_title
        self._use_permanent_title = other._use_permanent_title
        self._max_displayed_items = other._max_displayed_items
        self._items = [item._clone() for item in other._items]
        self._item_clicked_callback = other._item_clicked_callback


class _DropdownItem(object):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_DropdownItem, self).__init__()
        self._name = ""
        self._close_on_selected = True
        self._selected = False

    def _copy_values_deep(self, other):
        self._name = other._name
        self._close_on_selected = other._close_on_selected
        self._selected = other._selected

    def _clone(self):
        other = _DropdownItem._create()
        other._copy_values_deep(self)
        return other


class _Image(_UIBase):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        from nanome.util import Color, enums
        super(_Image, self).__init__()
        self._file_path = ""
        self._color = Color.White()
        self._scaling_option = enums.ScalingOptions.stretch
        self._pressed_callback = None
        self._held_callback = None
        self._released_callback = None

    def _on_image_pressed(self, x, y):
        if self._pressed_callback != None:
            self._pressed_callback(self, x, y)

    def _on_image_held(self, x, y):
        if self._held_callback != None:
            self._held_callback(self, x, y)

    def _on_image_released(self, x, y):
        if self._released_callback != None:
            self._released_callback(self, x, y)

    def _register_pressed_callback(self, func):
        from nanome.api.ui import messages
        if func == None and self._pressed_callback == None:  # Low hanging filter but there may be others
            return
        self._send_hook(messages.UIHook.Type.image_pressed)
        self._pressed_callback = func

    def _register_held_callback(self, func):
        from nanome.api.ui import messages
        if func == None and self._held_callback == None:  # Low hanging filter but there may be others
            return
        self._send_hook(messages.UIHook.Type.image_held)
        self._held_callback = func

    def _register_released_callback(self, func):
        from nanome.api.ui import messages
        if func == None and self._released_callback == None:  # Low hanging filter but there may be others
            return
        self._send_hook(messages.UIHook.Type.image_released)
        self._released_callback = func

    def _send_hook(self, hook_type):
        try:
            plugin_network = network.PluginNetwork._instance
            hook_ui_callback = enums.Messages.hook_ui_callback
            plugin_network.send(
                hook_ui_callback,
                (hook_type, self._content_id),
                False)
        except:
            logger.error("Could not register hook")

    def _copy_values_deep(self, other):
        super()._copy_values_deep(other)
        self._color = other._color
        self._scaling_option = other._scaling_option
        self._file_path = other._file_path
        self._pressed_callback = other._pressed_callback
        self._held_callback = other._held_callback
        self._released_callback = other._released_callback


class _Label(_UIBase):

    @property
    def HorizAlignOptions(self):
        import nanome
        return nanome.util.enums.HorizAlignOptions

    @property
    def VertAlignOptions(self):
        import nanome
        return nanome.util.enums.VertAlignOptions

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Label, self).__init__()
        from nanome.util import enums, Color
        self._text_value = ""
        self._text_vertical_align = enums.VertAlignOptions.Top
        self._text_horizontal_align = enums.HorizAlignOptions.Left
        self._text_auto_size = True
        self._text_max_size = 1.0
        self._text_min_size = 0.0
        self._text_size = 1.0
        self._text_color = Color.White()
        self._text_bold = False
        self._text_italic = False
        self._text_underlined = False

    def _copy_values_deep(self, other):
        super(_Label, self)._copy_values_deep(other)
        self._text_value = other._text_value
        self._text_vertical_align = other._text_vertical_align
        self._text_horizontal_align = other._text_horizontal_align
        self._text_auto_size = other._text_auto_size
        self._text_max_size = other._text_max_size
        self._text_min_size = other._text_min_size
        self._text_size = other._text_size
        self._text_color = other._text_color
        self._text_bold = other._text_bold
        self._text_italic = other._text_italic
        self._text_underlined = other._text_underlined


class _LayoutNode(object):

    @classmethod
    def _create(cls):
        return cls()

    id_gen = 0

    def __init__(self, name="node"):
        # protocol vars
        from nanome.util import enums
        self._id = _LayoutNode.id_gen
        self._enabled = True
        self._layer = 0
        self._layout_orientation = enums.LayoutTypes.vertical
        self._sizing_type = enums.SizingTypes.expand
        self._sizing_value = 1.0
        self._forward_dist = 0.0
        self._padding_type = enums.PaddingTypes.fixed
        self._padding = (0.0, 0.0, 0.0, 0.0)
        self._children = []
        self._content = None
        # API
        self._name = name
        self._parent = None
        _LayoutNode.id_gen += 1

    def _get_children(self):
        return self._children

    def _get_content(self):
        return self._content

    def _set_content(self, ui_content):
        # add to curr parent
        self._content = ui_content

    def _remove_content(self):
        self._content = None

    def _add_child(self, child_node):
        # remove from old parent
        if (child_node._parent != None):
            child_node._parent._remove_child(child_node)
        # add to curr parent
        self._children.append(child_node)
        child_node._parent = self

    def _remove_child(self, child_node):
        if child_node in self._children:
            self._children.remove(child_node)
            child_node._parent = None

    def _clear_children(self):
        for child in self._children:
            child._parent = None
        self._children = []

    def copy_values_shallow(self, other):
        """Copy node formatting, but ignore children or content."""
        exclude_fields = ["_children", "_content", "_id", "_parent", 'io']
        for field in other.__dict__:
            if field not in exclude_fields:
                setattr(self, field, getattr(other, field))

    def _copy_values_deep(self, other):
        self.copy_values_shallow(other)
        if (other._content != None):
            self._content = other._content._clone()
        for child in other._children:
            self._children.append(child._clone())

    def _clone(self):
        result = _LayoutNode._create()
        result._copy_values_deep(self)
        return result

# region non-api functions
    def _find_content(self, content_id):
        found_val = None
        content = self._content
        if self._content != None and content._content_id == content_id:
            return content

        if isinstance(content, _UIList):
            for node in content.items:
                found_val = node._find_content(content_id)
                if found_val != None:
                    return found_val

        for child in self._children:
            found_val = child._find_content(content_id)
            if found_val != None:
                return found_val
        return None

    def _append_all_content(self, all_content):
        """Recursively update all_content list with nested content."""
        if (self._content != None):
            all_content.append(self._content)
        for child in self._children:
            child._append_all_content(all_content)
        return all_content

    def _append_all_nodes(self, all_nodes):
        """Recursively update all_nodes list with nested nodes."""
        all_nodes.append(self)
        for child in self._children:
            child._append_all_nodes(all_nodes)
        return all_nodes

# endregion


class _LoadingBar(_UIBase):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_LoadingBar, self).__init__()
        self._percentage = 0.0
        self._title = ""
        self._description = ""
        self._failure = False

    def _copy_values_deep(self, other):
        super(_LoadingBar, self)._copy_values_deep(other)
        self._percentage = other._percentage
        self._title = other._title
        self._description = other._description
        self._failure = other._failure


class _Menu(object):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self, index=0, title="title"):
        # Protocol
        self._enabled = True
        self._title = title
        self._locked = False
        self._width = 0.7
        self._height = 0.6
        self._index = index
        # self.all_layout_nodes[]
        # self.all_contents[]

        # API
        self._root = _LayoutNode._create()
        self._opened_callback = lambda self: None
        self._closed_callback = lambda self: None

# region callback
    def _on_closed_callback(self):
        self._closed_callback(self)

    def _on_opened_callback(self):
        self._opened_callback(self)

# endregion

    def _find_content(self, content_id):
        return self._root._find_content(content_id)

    def _get_all_content(self):
        all_content = []
        self._root._append_all_content(all_content)
        return all_content

    def _get_all_nodes(self):
        all_nodes = []
        self._root._append_all_nodes(all_nodes)
        return all_nodes

    def _copy_data(self, other):
        self._enabled = other._enabled
        self._title = other._title
        self._locked = other._locked
        self._width = other._width
        self._height = other._height
        self._index = other._index


class _Mesh(_UIBase):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Mesh, self).__init__()
        from nanome.util import Color
        self._mesh_color = Color.Gray()

    def _copy_values_deep(self, other):
        super(_Mesh, self)._copy_values_deep(other)
        self._mesh_color = other._mesh_color


class _Slider(_UIBase):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        # Protocol
        super(_Slider, self).__init__()
        self._current_value = 0.0
        self._min_value = 0.0
        self._max_value = 1.0
        # API
        self._changed_callback = lambda self: None
        self._released_callback = lambda self: None

    def _on_slider_changed(self):
        self._changed_callback(self)

    def _on_slider_released(self):
        self._released_callback(self)

    def _copy_values_deep(self, other):
        super(_Slider, self)._copy_values_deep(other)
        self._current_value = other._current_value
        self._min_value = other._min_value
        self._max_value = other._max_value


class _TextInput(_UIBase):

    @property
    def HorizAlignOptions(self):
        import nanome
        return nanome.util.enums.HorizAlignOptions

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        from nanome.util import Color, enums
        # Protocol
        super(_TextInput, self).__init__()
        self._max_length = 10
        self._placeholder_text = ""
        self._input_text = ""
        self._placeholder_text_color = Color.from_int(0x7C7F89FF)
        self._text_color = Color.Black()
        self._background_color = Color.White()
        self._text_size = 1.0
        self._text_horizontal_align = enums.HorizAlignOptions.Left
        self._padding_left = 0.015
        self._padding_right = 0.01
        self._padding_top = 0.0
        self._padding_bottom = 0.0
        self._multi_line = False
        self._password = False
        self._number = False
        # API
        self._changed_callback = lambda self: None
        self._submitted_callback = lambda self: None

    def _on_text_changed(self):
        self._changed_callback(self)

    def _on_text_submitted(self):
        self._submitted_callback(self)

    def _copy_values_deep(self, other):
        super(_TextInput, self)._copy_values_deep(other)
        self._max_length = other._max_length
        self._placeholder_text = other._placeholder_text
        self._input_text = other._input_text


__metaclass__ = type
# classes inherting from _UIBase are expected to also inherit UIBase separately.


class _UIList(_UIBase):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_UIList, self).__init__()
        self._items = []
        self._display_columns = 1
        self._display_rows = 10
        self._total_columns = 1
        self._unusable = False

    def _copy_values_deep(self, other):
        super(_UIList, self)._copy_values_deep(other)
        self._items = []
        for item in other._items:
            self._items.append(item.clone())
        self._display_columns = other._display_columns
        self._display_rows = other._display_rows
        self._total_columns = other._total_columns
        self._unusable = other._unusable
