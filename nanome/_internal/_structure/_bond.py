from . import _Base
from nanome.util import IntEnum

class _Bond(_Base):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Bond, self).__init__()
        self._molecular = _Bond.Molecular._create()
        self.__atom1 = None
        self.__atom2 = None

    def _get_atom1(self):
        return self.__atom1
    def _set_atom1(self, atom1):
        if self.__atom1 != None:
            self.__atom1._bonds.remove(self)
        atom1._bonds.append(self)
        self.__atom1 = atom1

    def _get_atom2(self):
        return self.__atom2
    def _set_atom2(self, atom2):
        if self.__atom2 != None:
            self.__atom2._bonds.remove(self)
        atom2._bonds.append(self)
        self.__atom2 = atom2

    class Molecular(object):
        @classmethod
        def _create(cls):
            return cls()

        def __init__(self):
            self._kind = _Bond.Kind.CovalentSingle

    class Kind(IntEnum):
        CovalentSingle = 1
        CovalentDouble = 2
        CovalentTriple = 3
        Hydrogen = 4
        HydrogenWater = 5