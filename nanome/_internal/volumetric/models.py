from nanome.util import Color


class _UnitCell(object):
    def __init__(self):
        from nanome.util import Vector3
        self._A = 0.0
        self._B = 0.0
        self._C = 0.0

        self._Alpha = 0.0
        self._Beta = 0.0
        self._Gamma = 0.0

        self._Origin = Vector3()


class _VolumeData(object):

    def __init__(self):
        from nanome.util import enums
        self._data = []

        self._width = 0
        self._height = 0
        self._depth = 0

        self._mean = 0.0
        self._rmsd = 0.0
        self._type = enums.VolumeType.default
        self._name = ""

        self._cell = _UnitCell()


class _VolumeLayer():
    def __init__(self):
        self._color = Color()
        self._rmsd = 0.0


class _VolumeProperties():

    def __init__(self):
        from nanome.util import enums
        self._visible = True
        self._boxed = True
        self._use_map_mover = True
        self._style = enums.VolumeVisualStyle.Mesh
        self._layers = []
