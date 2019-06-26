import nanome
from nanome.util import Color, Logs
from . import _Base

class _Residue(_Base):
    RibbonMode = nanome.util.enums.RibbonMode
    SecondaryStructure = nanome.util.enums.SecondaryStructure

    @classmethod
    def _create(cls):
        return cls()
    
    def __init__(self):
        super(_Residue, self).__init__()
        #molecular
        self._type = "ARG" #RESIDUEDATA
        self._serial = 1
        self._name = "res"
        self._secondary_structure = _Residue.SecondaryStructure.Unknown
        #rendering
        self._ribboned = True
        self._ribbon_size = 1.0
        self._ribbon_mode = _Residue.RibbonMode.SecondaryStructure
        self._ribbon_color = Color.Clear()
        self._labeled = False
        self._label_text = ""
        #children
        self._atoms = []
        self._bonds = []