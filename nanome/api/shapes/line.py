from nanome.util.enums import ShapeType
from . import Shape
from .anchor import Anchor


class Line(Shape):

    def __init__(self):
        super().__init__(ShapeType.Line)
        self._anchors = [Anchor(), Anchor()]
        self._thickness = 0.1
        self._dash_length = 0.4
        self._dash_distance = 0.1

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
