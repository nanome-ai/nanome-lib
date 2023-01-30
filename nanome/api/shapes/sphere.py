from nanome.util.enums import ShapeType
from . import Shape
from .anchor import Anchor


class Sphere(Shape):
    """
    | Represents a sphere. Can display a sphere in Nanome App.
    """

    def __init__(self):
        super(Sphere, self).__init__(ShapeType.Sphere)
        self._anchors = [Anchor()]
        self._radius = 1.0

    @property
    def radius(self):
        """
        | Radius of the sphere

        :param value: Radius of the sphere
        :type value: float
        """
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
