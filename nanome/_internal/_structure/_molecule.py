from . import _Base

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
        self.__conformer_count = 0
        self._names = [""]
        self._associateds = [""]

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
        if value > len(self._names):
            self._names.append(self._names[-1])
            self._associateds.append(self._associateds[-1])
        else:
            self._names = self._names[:value]
            self._associateds = self._associateds[:value]
            self._current_conformer = value - 1
        self.__conformer_count = value
    #endregion

    def _shallow_copy(self):
        molecule = _Molecule._create()
        self._current_conformer = 0
        self.__conformer_count = 0
        self._names = [""]
        self._associateds = [""]
        return molecule

    def _deep_copy(self):
        molecule = self._shallow_copy()
        for chain in self._chains:
            chain._deep_copy()
            molecule._add_chain(chain)
        return molecule
