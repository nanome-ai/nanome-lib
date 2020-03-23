from nanome.util import enums
from . import _UnitCell

class _VolumeData(object):
    VolumeType = enums.VolumeType

    def __init__(self):
        self._data = [] 

        self._width = 0
        self._height = 0
        self._depth = 0
        
        self._mean = 0.0
        self._rmsd = 0.0
        self._type = _VolumeData.VolumeType.default
        self._name = ""

        self._cell = _UnitCell()
