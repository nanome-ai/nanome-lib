from . import _UIBase
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
        #API
        self._pressed_callback = lambda _: None
        self._hover_callback = lambda _: None

    def _on_button_pressed (self):
        self._pressed_callback(self)

    def _on_button_hover (self):
        self._hover_callback(self)

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
    
    def _copy_values_deep(self, other):
        super(_Button, self)._copy_values_deep(other)
        self._selected = other._selected
        self._unusable = other._unusable
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
        self._pressed_callback = other._pressed_callback
        self._hover_callback = other._hover_callback