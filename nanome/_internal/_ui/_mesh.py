from . import _UIBase
from nanome.util import Color

class _Mesh(_UIBase):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Mesh, self).__init__()
        self._mesh_color = Color.Gray()
        
    def _copy_values_deep(self, other):
        super(_Mesh, self)._copy_values_deep(other)
        self._mesh_color = other._mesh_color

