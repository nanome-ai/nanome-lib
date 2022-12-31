from nanome.util.enums import ShapeType

from ._anchor import _Anchor
from ._shape import _Shape


class _Mesh(_Shape):
    def __init__(self):
        _Shape.__init__(self, ShapeType.Mesh)
        self._anchors = [_Anchor._create()]
        self._vertices = []
        self._normals = []
        self._colors = []
        self._triangles = []
        self._uv = []
        self._texture_path = ""
        self._unlit = False

    @classmethod
    def _create(cls):
        return cls()
