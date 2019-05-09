from nanome._internal._structure._molecule import _Molecule
from . import Base

class Molecule(_Molecule, Base):
    def __init__(self):
        super(Molecule, self).__init__()
        self.molecular = self._molecular
        
    def add_chain(self, chain):
        self._chains.append(chain)

    def remove_chain(self, chain):
        self._chains.remove(chain)

    class Molecular(_Molecule.Molecular):
        @property
        def name(self):
            return self._name
        @name.setter
        def name(self, value):
            self._name = value
    _Molecule.Molecular._create = Molecular

    #Generators:
    @property
    def chains(self):
        for chain in self._chains:
            yield chain

    @property
    def residues(self):
        for chain in self.chains:
            for residue in chain.residues:
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
_Molecule._create = Molecule