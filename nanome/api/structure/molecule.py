from nanome._internal._structure._molecule import _Molecule
from nanome.util import Logs
from . import Base

class Molecule(_Molecule, Base):
    def __init__(self):
        super(Molecule, self).__init__()
        self._molecular = Molecule.Molecular(self)
        
    def add_chain(self, chain):
        self._chains.append(chain)

    def remove_chain(self, chain):
        self._chains.remove(chain)

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

_Molecule._create = Molecule