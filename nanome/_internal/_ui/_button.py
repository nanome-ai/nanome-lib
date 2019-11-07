from . import _UIBase
from nanome.util import Vector3, Color
import nanome

class _Button(_UIBase):

    HorizAlignOptions = nanome.util.enums.HorizAlignOptions
    VertAlignOptions = nanome.util.enums.VertAlignOptions

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
        nanome._internal._network._ProcessNetwork._instance._send(
            nanome._internal._network._commands._callbacks._Messages.hook_ui_callback,
            (nanome._internal._network._commands._serialization._UIHook.Type.button_hover, self._content_id))
        self._hover_callback = func

    class ButtonText(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._active = True
            self._value_idle = "idle"
            self._value_selected = "selected"
            self._value_highlighted = "highlighted"
            self._value_selected_highlighted = "selected and highlighted"
            self._value_unusable = "unusable"
            self._auto_size = True
            self._min_size = 0.0
            self._max_size = 1.0
            self._size = 1.0
            self._underlined = False
            self._bolded = False
            self._vertical_align =  _Button.VertAlignOptions.Middle
            self._horizontal_align = _Button.HorizAlignOptions.Middle

    class ButtonIcon(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._active = False
            self._value_idle = ""
            self._value_selected = ""
            self._value_highlighted = ""
            self._value_selected_highlighted = ""
            self._value_unusable = ""
            self._color_idle = Color.White()
            self._color_selected = Color.White()
            self._color_highlighted = Color.White()
            self._color_selected_highlighted = Color.White()
            self._color_unusable = Color.White()
            self._sharpness = 0.5
            self._size = 1.0
            self._ratio = 0.5
            self._position = Vector3()
            self._rotation = Vector3()

    def _copy_values_deep(self, other):
        super(_Button, self)._copy_values_deep(other)
        # States
        self._selected = other._selected
        self._unusable = other._unusable
        # Text
        self._text._active = other._text._active
        self._text._value_idle = other._text._value_idle
        self._text._value_selected = other._text._value_selected
        self._text._value_highlighted = other._text._value_highlighted
        self._text._value_selected_highlighted = other._text._value_selected_highlighted
        self._text._value_unusable = other._text._value_unusable
        self._text._auto_size = other._text._auto_size
        self._text._min_size = other._text._min_size
        self._text._max_size = other._text._max_size
        self._text._size = other._text._size
        self._text._underlined = other._text._underlined
        self._text._bolded = other._text._bolded
        self._text._vertical_align = other._text._vertical_align
        self._text._horizontal_align = other._text._horizontal_align
        # Icon
        self._icon._active = other._icon._active
        self._icon._value_idle = other._icon._value_idle
        self._icon._value_selected = other._icon._value_selected
        self._icon._value_highlighted = other._icon._value_highlighted
        self._icon._value_selected_highlighted = other._icon._value_selected_highlighted
        self._icon._value_unusable = other._icon._value_unusable
        self._icon._color_idle = other._icon._color_idle
        self._icon._color_selected = other._icon._color_selected
        self._icon._color_highlighted = other._icon._color_highlighted
        self._icon._color_selected_highlighted = other._icon._color_selected_highlighted
        self._icon._color_unusable = other._icon._color_unusable
        self._icon._sharpness = other._icon._sharpness
        self._icon._size = other._icon._size
        self._icon._ratio = other._icon._ratio
        self._icon._position = other._icon._position
        self._icon._rotation = other._icon._rotation
        # Callbacks
        self._pressed_callback = other._pressed_callback
        self._hover_callback = other._hover_callback
