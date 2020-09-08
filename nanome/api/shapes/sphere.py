from . import Shape
from nanome.util.enums import ShapeType

class Sphere(Shape):
    def __init__(self, network):
        super().__init__(network, ShapeType.Sphere)

        self.__radius = 1.0

    @property
    def radius(self):
        return self.__radius
    @radius.setter
    def radius(self, value):
        self.__radius = value

    