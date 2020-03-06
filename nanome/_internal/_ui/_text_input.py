from . import _UIBase

class _TextInput(_UIBase):
        
    @classmethod
    def _create(cls):
        return cls()
        
    def __init__(self):
        #Protocol
        super(_TextInput, self).__init__()
        self._max_length = 10
        self._placeholder_text = "PlaceHolderText"
        self._input_text = ""
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