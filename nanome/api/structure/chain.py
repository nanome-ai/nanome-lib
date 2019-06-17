from nanome._internal._structure._chain import _Chain
from nanome.util import Logs
from . import Base

class Chain(_Chain, Base):
    def __init__(self):
        super(Chain, self).__init__()
        self._molecular = Chain.Molecular(self)

    def add_residue(self, residue):
        self._residues.append(residue)

    def remove_residue(self, residue):
        self._residues.remove(residue)

    #Generators:
    @property
    def residues(self):
        for residue in self._residues:
            yield residue

    @property
    def atoms(self):
        for residue in self.residues:
            for atom in residue.atoms:
                yield atom

    @property
    def bonds(self):
        for residue in self.residues:
            for bond in residue.bonds:
                yield bond

    #region all fields
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
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
        def name(self):
            return self.parent.name
        @name.setter
        def name(self, value):
            self.parent.name = value
    #endregion
_Chain._create = Chain