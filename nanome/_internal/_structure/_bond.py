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

    @property
    def _atom1(self):
        return self.__atom1

    @_atom1.setter
    def _atom1(self, value):
        if self.__atom1 is not None:
            self.__atom1._bonds.remove(self)
        value._bonds.append(self)
        self.__atom1 = value

    @property
    def _atom2(self):
        return self.__atom2

    @_atom2.setter
    def _atom2(self, value):
        if self.__atom2 is not None:
            self.__atom2._bonds.remove(self)
        value._bonds.append(self)
        self.__atom2 = value

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
