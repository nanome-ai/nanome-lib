from nanome.util.enums import ShapeType

from . import Shape
from .anchor import Anchor


class Mesh(Shape):
    """
    | Represents a mesh. Can display a mesh in Nanome App.
    """

    def __init__(self):
        super().__init__(ShapeType.Mesh)
        self._anchors = [Anchor()]
        self._vertices = []
        self._normals = []
        self._colors = []
        self._triangles = []
        self._uv = []
        self._texture_path = ""
        self._unlit = False

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

    @property
    def texture_path(self):
        """
        | Path to the texture mapped to the mesh, has to be png or jpeg

        :param value: Path to the texture
        :type value: string
        """
        return self._texture_path

    @texture_path.setter
    def texture_path(self, value):
        self._texture_path = value

    @property
    def unlit(self):
        """
        | Use unlit material

        :param value: unlit material
        :type value: bool
        """
        return self._unlit

    @unlit.setter
    def unlit(self, value):
        self._unlit = value
