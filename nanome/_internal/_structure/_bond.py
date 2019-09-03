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

    #region connections
    @property
    def _residue(self):
        return self._parent

    @property
    def _chain(self):
        parent = self._parent
        if parent:
            return parent._chain
        else:
            return None

    @property
    def _molecule(self):
        parent = self._parent
        if parent:
            return parent._molecule
        else:
            return None

    @property
    def _complex(self):
        parent = self._parent
        if parent:
            return parent._complex
        else:
            return None
    #endregion