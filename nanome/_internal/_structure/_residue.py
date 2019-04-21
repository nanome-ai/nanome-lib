from nanome.util import Color, Enum, Logs
from . import _Base

class _Residue(_Base):
    @classmethod
    def _create(cls):
        return cls()
    
    def __init__(self):
        super(_Residue, self).__init__()
        self._rendering = _Residue.Rendering._create()
        self._molecular = _Residue.Molecular._create()
        self._atoms = []
        self._bonds = []

    class Rendering(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._modified = False
            self._ribboned = True
            self._ribbon_size = 0.0
            self._ribbon_mode = _Residue.RibbonMode.AdaptiveTube 
            self._ribbon_color = Color.Clear()

    class Molecular(object):
        @classmethod
        def _create(cls):
            return cls()
        
        def __init__(self):
            self._type = "ARG" #RESIDUEDATA
            self._serial = 0
            self._name = "res"
            self._secondary_structure = _Residue.SecondaryStructure.Unknown

    class RibbonMode(Enum):
        SecondaryStructure = 0
        AdaptiveTube = 1
        Coil = 2

    class SecondaryStructure(Enum):
        Unknown = 0
        Coil = 1
        Sheet = 2
        Helix = 3

    def get_atom_iterator(self):
        iterator = _Residue.AtomIterator(self)
        return iter(iterator)

    class AtomIterator(object):
        def __init__(self, residue):
            self._residue = residue

        def __iter__(self):
            self._atom = iter(self._residue._atoms)
            return self

        def __next__(self):
            return next(self._atom)