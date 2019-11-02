from . import _UIBase
from nanome.util import Vector3, Color
import nanome
import copy

class _Button(_UIBase):

    HorizAlignOptions = nanome.util.enums.HorizAlignOptions
    VertAlignOptions = nanome.util.enums.VertAlignOptions
    ToolTipPositioning = nanome.util.enums.ToolTipPositioning

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Button, self).__init__()
        #PROTOCOL
        self._selected = False
        self._unusable = False
        self._text = _Button.ButtonText._create()
        self._icon = _Button.ButtonIcon._create()
        self._mesh = _Button.ButtonMesh._create()
        self._outline = _Button.ButtonOutline._create()
        self._tooltip = _Button.ButtonTooltip._create()
        #API
        self._pressed_callback = lambda _: None
        self._hover_callback = lambda _, __: None

    def _on_button_pressed(self):
        self._pressed_callback(self)

    def _on_button_hover(self, state):
        self._hover_callback(self, state)

    def _register_pressed_callback(self, func):
        self._pressed_callback = func

    def _register_hover_callback(self, func):
        self._hover_callback = func

    class ButtonText(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._active = True
            self._value = _MultiStateVariable("text")
            self._auto_size = True
            self._min_size = 0.0
            self._max_size = 1.0
            self._size = 1.0
            self._underlined = False
            self._ellipsis = True
            self._bolded = _MultiStateVariable(False)
            self._color = _MultiStateVariable(Color.Black())
            DEFAULT_VALUE = "TODO"
            self.padding_top = DEFAULT_VALUE
            self.padding_bottom = DEFAULT_VALUE
            self.padding_left = DEFAULT_VALUE
            self.padding_right = DEFAULT_VALUE
            self.line_spacing = DEFAULT_VALUE
            self._vertical_align =  _Button.VertAlignOptions.Middle
            self._horizontal_align = _Button.HorizAlignOptions.Middle

    class ButtonIcon(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._active = False
            self._value = _MultiStateVariable("")
            self._color = _MultiStateVariable(Color.White())
            self._sharpness = 0.5
            self._size = 1.0
            self._ratio = 0.5
            self._position = Vector3()
            self._rotation = Vector3()

    class ButtonMesh(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._active = False
            self._enabled = _MultiStateVariable(True)
            self._color = _MultiStateVariable(Color.White())

    class ButtonOutline(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            DEFAULT_VALUE = "TODO"
            self._active = False
            self._size = _MultiStateVariable(DEFAULT_VALUE)
            self._color = _MultiStateVariable(Color.White())

    class ButtonTooltip(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            DEFAULT_VALUE = "TODO"
            self._title = ""
            self._content = ""
            self._bounds = DEFAULT_VALUE
            self._positioning_target = _Button.ToolTipPositioning.right
            self._positioning_origin = _Button.ToolTipPositioning.top_left

    def _copy_values_deep(self, other):
        super(_Button, self)._copy_values_deep(other)
        # States
        self._selected = other._selected
        self._unusable = other._unusable
        # Text
        self._text._active = other._text._active
        self._text._value._copy(other._text._value)
        self._text._auto_size = other._text._auto_size
        self._text._min_size = other._text._min_size
        self._text._max_size = other._text._max_size
        self._text._size = other._text._size
        self._text._underlined = other._text._underlined
        self._text._ellipsis = other._text._ellipses
        self._text._bolded._copy(other._text._bolded)
        self._text._color._copy(other._text._color)
        self.padding_top = other.padding_top
        self.padding_bottom = other.padding_bottom
        self.padding_left = other.padding_left
        self.padding_right = other.padding_right
        self.line_spacing = other.line_spacing
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
        #Mesh
        self._mesh._active = other._mesh._active
        self._mesh._enabled._copy(self._mesh._enabled)
        self._mesh._color._copy(self._mesh._color)
        #Outline
        self._outline._active = other._outline._active
        self._outline._size._copy(other._outline._size)
        self._outline._color._copy(other._outline._color)
        #Tooltip
        self._tooltip._title = other._tooltip._title
        self._tooltip._content = other._tooltip._content
        self._tooltip._bounds = other._tooltip._bounds
        self._tooltip._positioning_target = other._tooltip._positioning_target
        self._tooltip._positioning_origin = other._tooltip._positioning_origin
        #Callbacks
        self._pressed_callback = other._pressed_callback
        self._hover_callback = other._hover_callback

class _MultiStateVariable(object):
    def __init__(self, default = None):
        self._set_all(default)

    def _set_all(self, value):
        self._idle = copy.deepcopy(value)
        self._highlighted = copy.deepcopy(value)
        self._selected = copy.deepcopy(value)
        self._selected_highlighted = copy.deepcopy(value)
        self._unusable = copy.deepcopy(value)

    def set_all(self, value):
        self.idle = copy.deepcopy(value)
        self.highlighted = copy.deepcopy(value)
        self.selected = copy.deepcopy(value)
        self.selected_highlighted = copy.deepcopy(value)
        self.unusable = copy.deepcopy(value)

    def _copy(self, other):
        self._idle = other._idle
        self._highlighted = other._highlighted
        self._selected = other._selected
        self._selected_highlighted = other._selected_highlighted
        self._unusable = other._unusable

    @property
    def idle(self):
        return self._idle
    
    @idle.setter
    def idle(self, value):
        self._idle = value

    @property
    def higlighted(self):
        return self._higlighted
    
    @higlighted.setter
    def higlighted(self, value):
        self._higlighted = value

    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, value):
        self._selected = value

    @property
    def selected_highlighted(self):
        return self._selected_highlighted
    
    @selected_highlighted.setter
    def selected_highlighted(self, value):
        self._selected_highlighted = value

    @property
    def unusable(self):
        return self._unusable
    
    @unusable.setter
    def unusable(self, value):
        self._unusable = value