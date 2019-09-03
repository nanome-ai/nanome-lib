from . import _Base

class _Chain(_Base):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Chain, self).__init__()
        self._name = "chain"
        self._residues = []
        #Parent pointers
        self._molecule = None

    @property
    def _parent(self):
        return self._molecule

    @_parent.setter
    def _parent(self, value):
        self._molecule = value

    def _add_residue(self, residue):
        self._residues.append(residue)
        residue._chain = self

    def _remove_residue(self, residue):
        self._residues.remove(residue)
        residue._chain = None
    
    def _set_residues(self, residues):
        self._residues = residues
        for residue in residues:
            residue._chain = self