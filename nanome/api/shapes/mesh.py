from nanome._internal._shapes._mesh import _Mesh
from nanome.util.enums import ShapeType
from . import Shape


class Mesh(_Mesh, Shape):
    """
    | Represents a mesh. Can display a mesh in Nanome App.
    """

    def __init__(self):
        Shape.__init__(self, ShapeType.Mesh)
        _Mesh.__init__(self)

    # @property
    # def radius(self):
    #     """
    #     | Radius of the sphere

    #     :param value: Radius of the sphere
    #     :type value: float
    #     """
    #     return self._radius

    # @radius.setter
    # def radius(self, value):
    #     self._radius = value


_Mesh._create = Mesh
