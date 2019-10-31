from . import _Base
from . import _helpers
import copy

class _Molecule(_Base):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Molecule, self).__init__()
        self._chains = []
        self._parent = None
        #conformers
        self._current_conformer = 0
        self.__conformer_count = 1
        self._names = [""]
        self._associateds = [dict()]

    def _add_chain(self, chain):
        self._chains.append(chain)
        chain._parent = self

    def _remove_chain(self, chain):
        self._chains.remove(chain)
        chain._parent = None
    
    def _set_chains(self, chains):
        self._chains = chains
        for chain in chains:
            chain._parent = self

    #region connections

    @property
    def _residues(self):
        for chain in self._chains:
            for residue in chain._residues:
                yield residue

    @property
    def _atoms(self):
        for residue in self._residues:
            for atom in residue._atoms:
                yield atom
                
    @property
    def _bonds(self):
        for residue in self._residues:
            for bond in residue._bonds:
                yield bond

    @property
    def _complex(self):
        return self._parent
    #endregion

    @property
    def _name(self):
        return self._names[self._current_conformer]
    
    @_name.setter
    def _name(self, value):
        self._names[self._current_conformer] = value

    @property
    def _associated(self):
        return self._associateds[self._current_conformer]
    
    @_associated.setter
    def _associated(self, value):
        self._associateds[self._current_conformer] = value

    #region conformers
    @property
    def _conformer_count(self):
        return self.__conformer_count
    
    @_conformer_count.setter
    def _conformer_count(self, value):
        curr_size = len(self._names)
        if value > curr_size:
            extension = value - curr_size
            self._names.extend([self._names[-1]]*(extension))
            copy_val = self._associateds[-1]
            self._associateds.extend([copy_val.copy() for i in range(extension)])
        else:
            self._names = self._names[:value]
            self._associateds = self._associateds[:value]
        self._current_conformer = min(self._current_conformer, value - 1)
        self.__conformer_count = value

        for atom in self._atoms:
            atom._resize_conformer(value)
        for bond in self._bonds:
            bond._resize_conformer(value)

    def _create_conformer(self, index):
        src = max(0, index-1)
        self._copy_conformer(src, index)

    def _move_conformer(self, src, dest):
        temp = self._names[src]
        self._names.insert(dest, temp)

        temp = self._associateds[src]
        self._associateds.insert(dest, temp)
        crcted = src + 1 if src > dest else src
        del self._names[crcted]
        del self._associateds[crcted]

        for atom in self._atoms:
            atom._move_conformer(src, dest)
        for bond in self._bonds:
            bond._move_conformer(src, dest)

    def _delete_conformer(self, index):
        del self._names[index]
        del self._associateds[index]
        for atom in self._atoms:
            atom._delete_conformer(index)
        for bond in self._bonds:
            bond._delete_conformer(index)
        self.__conformer_count -= 1
        self._current_conformer = min(self._current_conformer, self.__conformer_count-1)

    def _copy_conformer(self, src, index= None):
        if index is None:
            index = src+1
        value = self._names[src]
        self._names.insert(index, value)
        value = self._associateds[src].copy()
        self._associateds.insert(index, value)
        for atom in self._atoms:
            atom._copy_conformer(src, index)
        for bond in self._bonds:
            bond._copy_conformer(src, index)
        self.__conformer_count += 1

    #endregion

        #copies the structure. If conformer_number is not None it will only copy that conformer's data
    def _shallow_copy(self, conformer_number = None):
        molecule = _Molecule._create()
        if conformer_number == None:
            molecule._names = list(self._names)
            molecule._associateds = copy.deepcopy(self._associateds)
            molecule.__conformer_count = self.__conformer_count
            molecule._current_conformer = self._current_conformer
        else:
            molecule._name = self._names[conformer_number]
            molecule._associated = self._associateds[conformer_number]
            molecule.__conformer_count = 1
            molecule._current_conformer = 0
        return molecule

    def _deep_copy(self, conformer_number = None):
        return _helpers._copy._deep_copy_molecule(self, conformer_number)
