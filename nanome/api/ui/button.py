import nanome
from nanome._internal._ui import _Button
from . import UIBase

class Button(_Button, UIBase):
    HorizAlignOptions = nanome.util.enums.HorizAlignOptions
    VertAlignOptions = nanome.util.enums.VertAlignOptions

    def __init__(self, text = None, icon = None):
        # type: (str, str)
        _Button.__init__(self)
        UIBase.__init__(self)
        self.text = self._text
        self.icon = self._icon
        if (text != None):
            self.set_all_text(text)
        if (icon != None):
            self.set_all_icon(icon)

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

    def set_all_icon(self, icon):
        # type: (str)
        """
        | Sets the path to the icon for every state.
        | Enables the button icon

        :param icon: The path to the icon file
        :type icon: str
        """
        self.icon.active = True
        self.icon.value_idle = icon
        self.icon.value_selected = icon
        self.icon.value_highlighted = icon
        self.icon.value_selected_highlighted = icon
        self.icon.value_unusable = icon

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
            if type(value) is not str:
                value = str(value)
            self._value_idle = value

        @property
        def value_selected(self):
            # type: () -> str
            return self._value_selected
        @value_selected.setter
        def value_selected(self, value):
            # type: (str)
            if type(value) is not str:
                value = str(value)
            self._value_selected = value

        @property
        def value_highlighted(self):
            # type: () -> str
            return self._value_highlighted
        @value_highlighted.setter
        def value_highlighted(self, value):
            # type: (str)
            if type(value) is not str:
                value = str(value)
            self._value_highlighted = value

        @property
        def value_selected_highlighted(self):
            # type: () -> str
            return self._value_selected_highlighted
        @value_selected_highlighted.setter
        def value_selected_highlighted(self, value):
            # type: (str)
            if type(value) is not str:
                value = str(value)
            self._value_selected_highlighted = value

        @property
        def value_unusable(self):
            # type: () -> str
            return self._value_unusable
        @value_unusable.setter
        def value_unusable(self, value):
            # type: (str)
            if type(value) is not str:
                value = str(value)
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

    class ButtonIcon(_Button.ButtonIcon):
        @property
        def active(self):
            return self._active
        @active.setter
        def active(self, value):
            self._active = value

        @property
        def value_idle(self):
            return self._value_idle
        @value_idle.setter
        def value_idle(self, value):
            if type(value) is not str:
                value = str(value)
            self._value_idle = value

        @property
        def value_selected(self):
            return self._value_selected
        @value_selected.setter
        def value_selected(self, value):
            if type(value) is not str:
                value = str(value)
            self._value_selected = value

        @property
        def value_highlighted(self):
            return self._value_highlighted
        @value_highlighted.setter
        def value_highlighted(self, value):
            if type(value) is not str:
                value = str(value)
            self._value_highlighted = value

        @property
        def value_selected_highlighted(self):
            return self._value_selected_highlighted
        @value_selected_highlighted.setter
        def value_selected_highlighted(self, value):
            if type(value) is not str:
                value = str(value)
            self._value_selected_highlighted = value

        @property
        def value_unusable(self):
            return self._value_unusable
        @value_unusable.setter
        def value_unusable(self, value):
            if type(value) is not str:
                value = str(value)
            self._value_unusable = value

        @property
        def color_idle(self):
            return self._color_idle
        @color_idle.setter
        def color_idle(self, value):
            self._color_idle = value

        @property
        def color_selected(self):
            return self._color_selected
        @color_selected.setter
        def color_selected(self, value):
            self._color_selected = value

        @property
        def color_highlighted(self):
            return self._color_highlighted
        @color_highlighted.setter
        def color_highlighted(self, value):
            self._color_highlighted = value

        @property
        def color_selected_highlighted(self):
            return self._color_selected_highlighted
        @color_selected_highlighted.setter
        def color_selected_highlighted(self, value):
            self._color_selected_highlighted = value

        @property
        def color_unusable(self):
            return self._color_unusable
        @color_unusable.setter
        def color_unusable(self, value):
            self._color_unusable = value

        @property
        def sharpness(self):
            return self._sharpness
        @sharpness.setter
        def sharpness(self, value):
            self._sharpness = value

        @property
        def size(self):
            return self._size
        @size.setter
        def size(self, value):
            self._size = value

        @property
        def ratio(self):
            return self._ratio
        @ratio.setter
        def ratio(self, value):
            self._ratio = value

        @property
        def position(self):
            return self._position
        @position.setter
        def position(self, value):
            self._position = value

        @property
        def rotation(self):
            return self._rotation
        @rotation.setter
        def rotation(self, value):
            self._rotation = value
    _Button.ButtonIcon._create = ButtonIcon
_Button._create = Button