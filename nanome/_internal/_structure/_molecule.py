from . import _Base

class _Molecule(_Base):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Molecule, self).__init__()
        self._name = "molecule"
        self._associated = {}
        self._chains = []

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