from nanome._internal._shapes._sphere import _Sphere
from nanome.util.enums import ShapeType
from . import Shape

class Sphere(_Sphere, Shape):
    def __init__(self):
        _Sphere.__init__(self)
        Shape.__init__(self, ShapeType.Sphere)

    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, value):
        self._radius = value