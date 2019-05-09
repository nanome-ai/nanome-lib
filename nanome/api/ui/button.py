from nanome._internal._ui import _Button
from nanome.util.text_settings import VertAlignOptions, HorizAlignOptions
from . import UIBase

class Button(_Button, UIBase):
    def __init__(self, text = None):
        # type: (str, str)
        _Button.__init__(self)
        UIBase.__init__(self)
        self.text = self._text
        if (text != None):
            self.set_all_text(text)

    def register_pressed_callback(self, func):
        _Button._register_pressed_callback(self, func)

    def set_all_text(self, text):
        # type: (str)
        """
        | Sets the text value of every state to the given text.

        :param text: The text to display on the button
        :type text: str
        """
        self.text.value_idle = text
        self.text.value_selected = text
        self.text.value_highlighted = text
        self.text.value_selected_highlighted = text
        self.text.value_unusable = text

    @property
    def selected(self):
        # type: () -> bool
        return self._selected
    @selected.setter
    def selected(self, value):
        # type: (bool)
        self._selected = value

    @property
    def unusable(self):
        # type: () -> bool
        return self._unusable
    @unusable.setter
    def unusable(self, value):
        # type: (bool)
        self._unusable = value

    class ButtonText(_Button.ButtonText):
        @property
        def active(self):
            # type: () -> bool
            return self._active
        @active.setter
        def active(self, value):
            # type: (bool)
            self._active = value

        @property
        def value_idle(self):
            # type: () -> str
            return self._value_idle
        @value_idle.setter
        def value_idle(self, value):
            # type: (str)
            self._value_idle = value

        @property
        def value_selected(self):
            # type: () -> str
            return self._value_selected
        @value_selected.setter
        def value_selected(self, value):
            # type: (str)
            self._value_selected = value

        @property
        def value_highlighted(self):
            # type: () -> str
            return self._value_highlighted
        @value_highlighted.setter
        def value_highlighted(self, value):
            # type: (str)
            self._value_highlighted = value

        @property
        def value_selected_highlighted(self):
            # type: () -> str
            return self._value_selected_highlighted
        @value_selected_highlighted.setter
        def value_selected_highlighted(self, value):
            # type: (str)
            self._value_selected_highlighted = value

        @property
        def value_unusable(self):
            # type: () -> str
            return self._value_unusable
        @value_unusable.setter
        def value_unusable(self, value):
            # type: (str)
            self._value_unusable = value

        @property
        def auto_size(self):
            # type: () -> bool
            return self._auto_size
        @auto_size.setter
        def auto_size(self, value):
            # type: (bool)
            self._auto_size = value

        @property
        def min_size(self):
            # type: () -> float
            return self._min_size
        @min_size.setter
        def min_size(self, value):
            # type: (float)
            self._min_size = value

        @property
        def max_size(self):
            # type: () -> float
            return self._max_size
        @max_size.setter
        def max_size(self, value):
            # type: (float)
            self._max_size = value

        @property
        def size(self):
            # type: () -> float
            return self._size
        @size.setter
        def size(self, value):
            # type: (float)
            self._size = value

        @property
        def underlined(self):
            # type: () -> bool
            return self._underlined
        @underlined.setter
        def underlined(self, value):
            # type: (bool)
            self._underlined = value

        @property
        def bolded(self):
            # type: () -> bool
            return self._bolded
        @bolded.setter
        def bolded(self, value):
            # type: (bool)
            self._bolded = value

        @property
        def vertical_align(self):
            # type: () -> VertAlignOptions
            return self._vertical_align
        @vertical_align.setter
        def vertical_align(self, value):
            # type: (VertAlignOptions)
            self._vertical_align = value

        @property
        def horizontal_align(self):
            # type: () -> HorizAlignOptions
            return self._horizontal_align
        @horizontal_align.setter
        def horizontal_align(self, value):
            # type: (HorizAlignOptions)
            self._horizontal_align = value
    _Button.ButtonText._create = ButtonText
_Button._create = Button