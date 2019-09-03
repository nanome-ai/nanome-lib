from . import _Base
import nanome

class _Bond(_Base):
    Kind = nanome.util.enums.Kind

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Bond, self).__init__()
        self._kind = _Bond.Kind.CovalentSingle
        self.__atom1 = None
        self.__atom2 = None
        #Parent pointers
        self._residue = None

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

    @property
    def _parent(self):
        return self._residue

    @_parent.setter
    def _parent(self, value):
        self._residue = value