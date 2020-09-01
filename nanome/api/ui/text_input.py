from nanome._internal._ui import _TextInput
from . import UIBase

class TextInput(_TextInput, UIBase):
    HorizAlignOptions = nanome.util.enums.HorizAlignOptions

    def __init__(self):
        # type: (str)
        _TextInput.__init__(self)
        UIBase.__init__(self)

    @property
    def max_length(self):
        # type: () -> int
        return self._max_length
    @max_length.setter
    def max_length(self, value):
        # type: (int)
        self._max_length = value

    @property
    def placeholder_text(self):
        # type: () -> str
        return self._placeholder_text
    @placeholder_text.setter
    def placeholder_text(self, value):
        # type: (str)
        if type(value) is not str:
            value = str(value)
        self._placeholder_text = value

    @property
    def input_text(self):
        # type: () -> str
        return self._input_text
    @input_text.setter
    def input_text(self, value):
        # type: (str)
        if type(value) is not str:
            value = str(value)
        self._input_text = value

    @property
    def placeholder_text_color(self):
        # type: () -> Color
        return self._placeholder_text_color
    @placeholder_text_color.setter
    def placeholder_text_color(self, value):
        #type: (Color)
        self._placeholder_text_color = value

    @property
    def text_color(self):
        # type: () -> Color
        return self._text_color
    @text_color.setter
    def text_color(self, value):
        #type: (Color)
        self._text_color = value

    @property
    def background_color(self):
        # type: () -> Color
        return self._background_color
    @background_color.setter
    def background_color(self, value):
        #type: (Color)
        self._background_color = value

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = value

    @property
    def number(self):
        return self._number
    
    @number.setter
    def number(self, value):
        self._number = value

    def register_changed_callback(self, func):
        """
        | Registers a function to be called whenever the text input is changed. 
        | The function must take a text input as its only parameter.

        :param func: The function that will be called when the text input is changed.
        :type text: FunctionType
        """
        self._changed_callback = func

    def register_submitted_callback(self, func):
        """
        | Registers a function to be called whenever the user submits a text input. 
        | The function must take a text input as its only parameter.

        :param func: The function that will be called when the user submits a text input.
        :type text: FunctionType
        """
        self._submitted_callback = func

_TextInput._create = TextInput
