from nanome._internal._shapes import _Line
from nanome.util.enums import ShapeType
from . import Shape


class Line(_Line, Shape):
    def __init__(self):
        Shape.__init__(self, ShapeType.Line)
        _Line.__init__(self)

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self, value):
        self._anchors = value

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value

    @property
    def dash_length(self):
        return self._dash_length

    @dash_length.setter
    def dash_length(self, value):
        self._dash_length = value

    @property
    def dash_distance(self):
        return self._dash_distance

    @dash_distance.setter
    def dash_distance(self, value):
        self._dash_distance = value

_Line._create = Line