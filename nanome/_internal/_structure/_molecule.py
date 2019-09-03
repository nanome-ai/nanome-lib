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
        #Parent pointers
        self._complex = None

    @property
    def _parent(self):
        return self._complex

    @_parent.setter
    def _parent(self, value):
        self._complex = value

    def _add_chain(self, chain):
        self._chains.append(chain)
        chain._molecule = self

    def _remove_chain(self, chain):
        self._chains.remove(chain)
        chain._molecule = None
    
    def _set_chains(self, chains):
        self._chains = chains
        for chain in chains:
            chain._molecule = self