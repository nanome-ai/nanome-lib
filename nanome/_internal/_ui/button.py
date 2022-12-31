from . import _UIBase
from nanome.util import Vector3, Color
import nanome
from copy import deepcopy


class _Button(_UIBase):

    HorizAlignOptions = nanome.util.enums.HorizAlignOptions
    VertAlignOptions = nanome.util.enums.VertAlignOptions
    ToolTipPositioning = nanome.util.enums.ToolTipPositioning

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
        if func == None and self._hover_callback == None:  # Low hanging filter but there may be others
            return
        try:
            nanome._internal._network.PluginNetwork._instance._send(
                nanome._internal._network._commands._callbacks._Messages.hook_ui_callback,
                (nanome._internal._network._commands._serialization._UIHook.Type.button_hover, self._content_id),
                False)
        except:
            nanome.util.Logs.error("Could not register hook")
        self._hover_callback = func

    class _ButtonText(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
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
            self._vertical_align = _Button.VertAlignOptions.Middle
            self._horizontal_align = _Button.HorizAlignOptions.Middle

    class _ButtonIcon(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
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
            self._active = False
            self._enabled = _Button._MultiStateVariable._create(True)
            self._color = _Button._MultiStateVariable._create(Color.Black())

    class _ButtonOutline(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
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
            self._active = False
            self._on_color = Color.from_int(0x00FFD5FF)
            self._off_color = Color.from_int(0x727272FF)

    class _ButtonTooltip(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._title = ""
            self._content = ""
            self._bounds = Vector3(1.73, .6, .05)
            self._positioning_target = _Button.ToolTipPositioning.right
            self._positioning_origin = _Button.ToolTipPositioning.top_left

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
            self._highlighted = deepcopy(highlighted) or deepcopy(default) or self._highlighted
            self._selected = deepcopy(selected) or deepcopy(default) or self._selected
            self._selected_highlighted = deepcopy(selected_highlighted) or deepcopy(selected) or deepcopy(default) or self._selected_highlighted
            self._unusable = deepcopy(unusable) or deepcopy(default) or self._unusable

        def _copy(self, other):
            self._idle = other._idle
            self._highlighted = other._highlighted
            self._selected = other._selected
            self._selected_highlighted = other._selected_highlighted
            self._unusable = other._unusable
