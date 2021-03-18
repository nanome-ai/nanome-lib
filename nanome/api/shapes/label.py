from nanome._internal._shapes import _Label
from nanome.util.enums import ShapeType
from . import Shape


class Label(_Label, Shape):
    def __init__(self):
        Shape.__init__(self, ShapeType.Label)
        _Label.__init__(self)

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self, value):
        self._anchors = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size = value

_Label._create = Label