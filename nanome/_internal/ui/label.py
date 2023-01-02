from . import _UIBase
from nanome.util.color import Color


class _Label(_UIBase):

    @property
    def HorizAlignOptions(self):
        import nanome
        return nanome.util.enums.HorizAlignOptions

    @property
    def VertAlignOptions(self):
        import nanome
        return nanome.util.enums.VertAlignOptions

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Label, self).__init__()
        from nanome.util import enums
        self._text_value = ""
        self._text_vertical_align = enums.VertAlignOptions.Top
        self._text_horizontal_align = enums.HorizAlignOptions.Left
        self._text_auto_size = True
        self._text_max_size = 1.0
        self._text_min_size = 0.0
        self._text_size = 1.0
        self._text_color = Color.White()
        self._text_bold = False
        self._text_italic = False
        self._text_underlined = False

    def _copy_values_deep(self, other):
        super(_Label, self)._copy_values_deep(other)
        self._text_value = other._text_value
        self._text_vertical_align = other._text_vertical_align
        self._text_horizontal_align = other._text_horizontal_align
        self._text_auto_size = other._text_auto_size
        self._text_max_size = other._text_max_size
        self._text_min_size = other._text_min_size
        self._text_size = other._text_size
        self._text_color = other._text_color
        self._text_bold = other._text_bold
        self._text_italic = other._text_italic
        self._text_underlined = other._text_underlined
