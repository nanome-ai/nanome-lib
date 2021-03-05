import nanome
from . import _UIBase
from nanome.util import Color

class _TextInput(_UIBase):
    HorizAlignOptions = nanome.util.enums.HorizAlignOptions
        
    @classmethod
    def _create(cls):
        return cls()
        
    def __init__(self):
        #Protocol
        super(_TextInput, self).__init__()
        self._max_length = 10
        self._placeholder_text = ""
        self._input_text = ""
        self._placeholder_text_color = Color.from_int(0x7C7F89FF)
        self._text_color = Color.Black()
        self._background_color = Color.White()
        self._text_size = 1.0
        self._text_horizontal_align = _TextInput.HorizAlignOptions.Left
        self._padding_left = 0.015
        self._padding_right = 0.01
        self._padding_top = 0.0
        self._padding_bottom = 0.0
        self._multi_line = False
        self._password = False
        self._number = False
        #API
        self._changed_callback = lambda self: None
        self._submitted_callback = lambda self: None

    def _on_text_changed (self):
        self._changed_callback(self)
    
    def _on_text_submitted (self):
        self._submitted_callback(self)

    def _copy_values_deep(self, other):
        super(_TextInput, self)._copy_values_deep(other)
        self._max_length = other._max_length
        self._placeholder_text = other._placeholder_text
        self._input_text = other._input_text