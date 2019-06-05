import nanome
from nanome.util import Logs
from nanome._internal._structure._bond import _Bond
from . import Base


class Bond(_Bond, Base):
    """
    Represents a Bond between two atoms
    """
    Kind = nanome.util.enums.Kind
    
    def __init__(self):
        super(Bond, self).__init__()
        self._molecular = Bond.Molecular(self)

    @property
    def atom1(self):
        """
        First atom linked by this bond

        :type: :class:`~nanome.api.structure.atom.Atom`
        """
        return self._atom1

    @atom1.setter
    def atom1(self, value):
        self._atom1 = value

    @property
    def atom2(self):
        """
        Second atom linked by this bond

        :type: :class:`~nanome.api.structure.atom.Atom`
        """
        return self._atom2

    @atom2.setter
    def atom2(self, value):
        self._atom2 = value

    #region all fields
    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, value):
        self._kind = value
    #endregion

    #region deprecated
    @property
    @Logs.deprecated()
    def molecular(self):
        return self._molecular

    class Molecular(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def kind(self):
            return self.parent.kind

        @kind.setter
        def kind(self, value):
            self.parent.kind = value
    #endregion
_Bond._create = Bond
