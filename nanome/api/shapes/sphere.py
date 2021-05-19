from nanome._internal._shapes._sphere import _Sphere
from nanome.util.enums import ShapeType
from . import Shape

class Sphere(Shape):
    """
    | Represents a sphere. Can display a sphere in Nanome App.
    """
    def __init__(self):
        Shape.__init__(self, ShapeType.Sphere)
        _Sphere.__init__(self)

    @property
    def radius(self):
        """
        | Get radius of the sphere

        :rtype: float
        """
        return self._radius
    @radius.setter
    def radius(self, value):
        """
        | Set radius of the sphere

        :param value: Radius of the sphere
        :type value: float
        """
        self._radius = value
_Sphere._create = Sphere
