from ._anchor import _Anchor
from ._shape import _Shape
from nanome.util.enums import ShapeType


class _Label(_Shape):
    def __init__(self):
        _Shape.__init__(self, ShapeType.Label)
        self._anchors = [_Anchor._create()]
        self._text = ""
        self._font_size = .5

    @classmethod
    def _create(cls):
        return cls()
