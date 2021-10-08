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

    @property
    def vertices(self):
        """
        | Vertices of the mesh, 3 float per vertex

        :param value: Vertices of the mesh
        :type value: Array of float
        """
        return self._vertices

    @vertices.setter
    def vertices(self, value):
        self._vertices = value

    @property
    def normals(self):
        """
        | Normals for each vertex, 3 float per normal

        :param value: Normals of the mesh
        :type value: Array of float
        """
        return self._normals

    @normals.setter
    def normals(self, value):
        self._normals = value

    @property
    def triangles(self):
        """
        | Triangles of the mesh, 3 int per triangle

        :param value: Triangles of the mesh
        :type value: Array of int
        """
        return self._triangles

    @triangles.setter
    def triangles(self, value):
        self._triangles = value

    @property
    def colors(self):
        """
        | Colors of the mesh, 4 float per vertex

        :param value: Colors of the mesh
        :type value: Array of float
        """
        return self._colors

    @colors.setter
    def colors(self, value):
        self._colors = value

    @property
    def uv(self):
        """
        | UV of the mesh, 2 float per vertex

        :param value: UV of the mesh
        :type value: Array of float
        """
        return self._uv

    @uv.setter
    def uv(self, value):
        self._uv = value


_Mesh._create = Mesh
