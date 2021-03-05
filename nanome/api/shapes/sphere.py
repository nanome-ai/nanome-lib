from . import Shape
from .anchor import Anchor
from nanome.util.enums import ShapeType

class Sphere(Shape):
    def __init__(self, network):
        super().__init__(network, ShapeType.Sphere)
        self._anchors = [Anchor()]
        self._radius = 1.0

    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, value):
        self._radius = value