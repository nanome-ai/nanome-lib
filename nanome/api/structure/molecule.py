from nanome._internal._structure._molecule import _Molecule
from nanome.util import Logs
from . import Base

class Molecule(_Molecule, Base):
    def __init__(self):
        super(Molecule, self).__init__()
        self._molecular = Molecule.Molecular(self)
        
    def add_chain(self, chain):
        chain.index = -1
        self._add_chain(chain)

    def remove_chain(self, chain):
        chain.index = -1
        self._remove_chain(chain)

    #region Generators:
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
    #endregion

    #region connections
    @property
    def complex(self):
        return self._complex
    #endregion

    #region all fields
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        if type(value) is not str:
            value = str(value)
        self._name = value

    @property
    def associated(self):
        return self._associated
    
    @associated.setter
    def associated(self, value):
        self._associated = value
    #endregion

    #region conformer stuff
    @property
    def names(self):
        return self._names
    
    @names.setter
    def names(self, value):
        if len(value) != self._conformer_count:
            raise ValueError("Length of associateds must match the conformer count of the molecule.")
        self._names = value

    @property
    def associateds(self):
        return self._associateds
    
    @associateds.setter
    def associateds(self, value):
        if len(value) != self._conformer_count:
            raise ValueError("Length of associateds must match the conformer count of the molecule.")
        self._associateds = value

    def set_conformer_count(self, count):
        self._conformer_count = count

    @property
    def conformer_count(self):
        return self._conformer_count

    def set_current_conformer(self, index):
        self._current_conformer = index

    @property
    def current_conformer(self):
        return self._current_conformer

    def create_conformer(self, index):
        self._create_conformer(index)

    def move_conformer(self, src, dest):
        self._move_conformer(src, dest)

    def delete_conformer(self, index):
        self._delete_conformer(index)

    def copy_conformer(self, src, index= None):
        self._copy_conformer(src, index)
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