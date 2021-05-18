import nanome
from nanome._internal._ui import _Label
from nanome.util.color import Color
from . import UIBase

class Label(_Label, UIBase):
    """
    | Represents a label that cannot be interacted with in a menu
    """
    HorizAlignOptions = nanome.util.enums.HorizAlignOptions
    VertAlignOptions = nanome.util.enums.VertAlignOptions

    def __init__(self, text = None):
        # type: (str, str)
        _Label.__init__(self)
        UIBase.__init__(self)
        if text != None:
            self.text_value = text
    @property
    def text_value(self):
        """
        | The text to be displayed on the label

        :type: :class:`str`

        """
        # type: () -> str
        return self._text_value
    @text_value.setter
    def text_value(self, value):
        # type: (str)
        if type(value) is not str:
            value = str(value)
        self._text_value = value

    @property
    def text_vertical_align(self):
        """
        | The vertical alignment of the text

        :type: :class:`~nanome.util.enums.VertAlignOptions`
        
        """
        # type: () -> VertAlignOptions
        return self._text_vertical_align
    @text_vertical_align.setter
    def text_vertical_align(self, value):
        # type: (VertAlignOptions)
        self._text_vertical_align = value

    @property
    def text_horizontal_align(self):
        """
        | The horizontal alignment of the text

        :type: :class:`~nanome.util.enums.HorizAlignOptions`
        
        """
        # type: () -> HorizAlignOptions
        return self._text_horizontal_align
    @text_horizontal_align.setter
    def text_horizontal_align(self, value):
        # type: (HorizAlignOptions)
        self._text_horizontal_align = value

    @property
    def text_auto_size(self):
        """
        | Whether or not to automatically size the label text

        :type: :class:`bool`
        
        """
        # type: () -> bool
        return self._text_auto_size
    @text_auto_size.setter
    def text_auto_size(self, value):
        # type: (bool)
        self._text_auto_size = value

    @property
    def text_max_size(self):
        """
        | The maximum font size the text will display
        | This is the upper bound for auto sizing.

        :type: :class:`float`
        
        """
        # type: () -> float
        return self._text_max_size
    @text_max_size.setter
    def text_max_size(self, value):
        # type: (float)
        self._text_max_size = value

    @property
    def text_min_size(self):
        """
        | The minimum font size the text will display
        | This is the lower bound for auto sizing.

        :type: :class:`float`
        
        """
        # type: () -> float
        return self._text_min_size
    @text_min_size.setter
    def text_min_size(self, value):
        # type: (float)
        self._text_min_size = value

    @property
    def text_size(self):
        """
        | The font size of the text displayed on this label

        :type: :class:`float`
        
        """
        # type: () -> float
        return self._text_size
    @text_size.setter
    def text_size(self, value):
        # type: (float)
        self._text_size = value

    @property
    def text_color(self):
        """
        | The color of the text on this label

        :type: :class:`~nanome.util.Color`
        
        """
        # type: () -> Color
        return self._text_color
    @text_color.setter
    def text_color(self, value):
        # type: (Color)
        self._text_color = value

    @property
    def text_bold(self):
        """
        | Whether or not the text on this label is bold

        :type: :class:`bool`
        
        """
        # type: () -> bool
        return self._text_bold
    @text_bold.setter
    def text_bold(self, value):
        # type: (bool)
        self._text_bold = value

    @property
    def text_italic(self):
        """
        | Whether or not the text on this label is italic

        :type: :class:`bool`
        
        """
        # type: () -> bool
        return self._text_italic
    @text_italic.setter
    def text_italic(self, value):
        # type: (bool)
        self._text_italic = value

    @property
    def text_underlined(self):
        """
        | Whether or not the text on this label is underlined

        :type: :class:`bool`
        
        """
        # type: () -> bool
        return self._text_underlined
    @text_underlined.setter
    def text_underlined(self, value):
        # type: (bool)
        self._text_underlined = value


_Label._create = Label
