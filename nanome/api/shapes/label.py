from nanome.util.enums import ShapeType
from . import Shape
from .anchor import Anchor


class Label(Shape):

    def __init__(self):
        super().__init__(ShapeType.Label)
        self._anchors = [Anchor()]
        self._text = ""
        self._font_size = .5

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
