from . import _Base

class _Molecule(_Base):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Molecule, self).__init__()
        self._chains = []

        #conformers
        self._current_conformer = 0
        self.__conformer_count = 0
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
            self._names.extend([self._names[-1]]*(value - curr_size))
            self._associateds.extend([self._associateds[-1]]*(value - curr_size))
        else:
            self._names = self._names[:value]
            self._associateds = self._associateds[:value]
        self._current_conformer = min(self._current_conformer, value - 1)
        self.__conformer_count = value
    #endregion