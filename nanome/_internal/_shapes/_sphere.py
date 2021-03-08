from ._anchor import _Anchor
from ._shape import _Shape
from nanome.util.enums import ShapeType


class _Sphere(_Shape):
    def __init__(self):
        _Shape.__init__(self, ShapeType.Sphere)
        self._anchors = [_Anchor._create()]
        self._radius = 1.0

    @classmethod
    def _create(cls):
        return cls()
