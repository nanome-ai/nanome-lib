from nanome._internal._structure._chain import _Chain
from . import Base

class Chain(_Chain, Base):
    def __init__(self):
        super(Chain, self).__init__()
        self.molecular = self._molecular

    def add_residue(self, residue):
        self._residues.append(residue)

    def remove_residue(self, residue):
        self._residues.remove(residue)

    class Molecular(_Chain.Molecular):
        @property
        def name(self):
            return self._name
        @name.setter
        def name(self, value):
            self._name = value
    _Chain.Molecular._create = Molecular

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

_Chain._create = Chain