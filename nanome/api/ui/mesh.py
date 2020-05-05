from nanome.util.color import Color
from . import UIBase
from nanome._internal._ui import _Mesh

class Mesh(_Mesh, UIBase):
    def __init__(self):
        # type: (_Mesh)
        _Mesh.__init__(self)
        UIBase.__init__(self)

    @property
    def mesh_color(self):
        # type: () -> Color
        return self._mesh_color
    @mesh_color.setter
    def mesh_color(self, value):
        # type: (Color)
        self._mesh_color = value

_Mesh._create = Mesh