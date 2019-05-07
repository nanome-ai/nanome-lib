from nanome._internal._structure._bond import _Bond
from . import Base

class Bond(_Bond, Base):
    """    
    Represents a Bond between two atoms

    :ivar molecular: Contains molecular informations about the Bond
    :vartype molecular: :class:`~nanome.api.structure.bond.Bond.Molecular`
    """

    def __init__(self):
        super(Bond, self).__init__()
        self.molecular = self._molecular

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

    class Molecular(object):
        @property
        def kind(self):
            return self._kind
        @kind.setter
        def kind(self, value):
            self._kind = value
    _Bond.Molecular._create = Molecular

_Bond._create = Bond