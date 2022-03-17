import nanome
from nanome._internal._ui import _TextInput
from . import UIBase


class TextInput(_TextInput, UIBase):
    """
    | Represents a text input, where the user can input text
    """
    HorizAlignOptions = nanome.util.enums.HorizAlignOptions

    def __init__(self):
        _TextInput.__init__(self)
        UIBase.__init__(self)

    @property
    def max_length(self):
        """
        | The character limit of the input string

        :type: :class:`int`
        """
        return self._max_length

    @max_length.setter
    def max_length(self, value):
        self._max_length = value

    @property
    def placeholder_text(self):
        """
        | The text to display when the input is empty

        :type: :class:`str`
        """
        return self._placeholder_text

    @placeholder_text.setter
    def placeholder_text(self, value):
        if type(value) is not str:
            value = str(value)
        self._placeholder_text = value

    @property
    def input_text(self):
        """
        | The string that has been entered into this text input

        :type: :class:`str`
        """
        return self._input_text

    @input_text.setter
    def input_text(self, value):
        if type(value) is not str:
            value = str(value)
        self._input_text = value

    @property
    def placeholder_text_color(self):
        """
        | Color of the placeholder text

        :type: :class:`~nanome.util.Color`
        """
        return self._placeholder_text_color

    @placeholder_text_color.setter
    def placeholder_text_color(self, value):
        self._placeholder_text_color = value

    @property
    def text_color(self):
        """
        | The color of the input text

        :type: :class:`~nanome.util.Color`
        """
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        self._text_color = value

    @property
    def background_color(self):
        """
        | The color of the background of this text input

        :type: :class:`~nanome.util.Color`
        """
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        self._background_color = value

    @property
    def text_size(self):
        """
        | The font size of the input and placeholder text

        :type: :class:`float`
        """
        return self._text_size

    @text_size.setter
    def text_size(self, value):
        self._text_size = value

    @property
    def text_horizontal_align(self):
        """
        | The horizontal alignment of the input and placeholder text

        :type: :class:`~nanome.util.enums.HorizAlignOptions`
        """
        return self._text_horizontal_align

    @text_horizontal_align.setter
    def text_horizontal_align(self, value):
        self._text_horizontal_align = value

    @property
    def padding_left(self):
        """
        | The left padding of the input and placeholder text

        :type: :class:`float`
        """
        return self._padding_left

    @padding_left.setter
    def padding_left(self, value):
        self._padding_left = value

    @property
    def padding_right(self):
        """
        | The right padding of the input and placeholder text

        :type: :class:`float`
        """
        return self._padding_right

    @padding_right.setter
    def padding_right(self, value):
        self._padding_right = value

    @property
    def padding_top(self):
        """
        | The top padding of the input and placeholder text

        :type: :class:`float`
        """
        return self._padding_top

    @padding_top.setter
    def padding_top(self, value):
        self._padding_top = value

    @property
    def padding_bottom(self):
        """
        | The bottom padding of the input and placeholder text

        :type: :class:`float`
        """
        return self._padding_bottom

    @padding_bottom.setter
    def padding_bottom(self, value):
        self._padding_bottom = value

    @property
    def password(self):
        """
        | Whether or not the input represents a password.
        | i.e. will display 123 as \*\*\* if true.

        :type: :class:`bool`
        """
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def number(self):
        """
        | Whether or not the input represents a number.
        | Will display the number keyboard if set to true.

        :type: :class:`bool`
        """
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    def register_changed_callback(self, func):
        """
        | Registers a function to be called whenever the text input is changed.
        | The function must take a text input as its only parameter.

        :param func: The function that will be called when the text input is changed.
        :type text: method (:class:`~nanome.ui.TextInput`) -> None
        """
        self._changed_callback = func

    def register_submitted_callback(self, func):
        """
        | Registers a function to be called whenever the user submits a text input.
        | The function must take a text input as its only parameter.

        :param func: The function that will be called when the user submits a text input.
        :type text: method (:class:`~nanome.ui.TextInput`) -> None
        """
        self._submitted_callback = func


_TextInput._create = TextInput
