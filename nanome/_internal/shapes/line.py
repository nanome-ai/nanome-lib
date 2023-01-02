from .anchor import _Anchor
from .shape import _Shape


class _Line(_Shape):
    def __init__(self):
        from nanome.util.enums import ShapeType
        _Shape.__init__(self, ShapeType.Line)
        self._anchors = [_Anchor._create(), _Anchor._create()]
        self._thickness = 0.1
        self._dash_length = 0.4
        self._dash_distance = 0.1

    @classmethod
    def _create(cls):
        return cls()
