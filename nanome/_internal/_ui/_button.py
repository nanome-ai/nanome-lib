from . import _UIBase
from nanome.util.text_settings import VertAlignOptions, HorizAlignOptions

class _Button(_UIBase):

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

    def _on_button_pressed (self):
        self._pressed_callback(self)

    def _register_pressed_callback(self, func):
        self._pressed_callback = func

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
            self._vertical_align =  VertAlignOptions.Middle
            self._horizontal_align = HorizAlignOptions.Middle
    
    def _copy_values_deep(self, other):
        super(_Button, self)._copy_values_deep(other)
        self._selected = other._selected
        self._unusable = other._unusable
        self.text._active = other.text._active
        self.text._value_idle = other.text._value_idle
        self.text._value_selected = other.text._value_selected
        self.text._value_highlighted = other.text._value_highlighted
        self.text._value_selected_highlighted = other.text._value_selected_highlighted
        self.text._value_unusable = other.text._value_unusable
        self.text._auto_size = other.text._auto_size
        self.text._min_size = other.text._min_size
        self.text._max_size = other.text._max_size
        self.text._size = other.text._size
        self.text._underlined = other.text._underlined
        self.text._bolded = other.text._bolded
        self.text._vertical_align = other.text._vertical_align
        self.text._horizontal_align = other.text._horizontal_align
        self._pressed_callback = other._pressed_callback