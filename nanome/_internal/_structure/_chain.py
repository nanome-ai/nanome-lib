from . import _Base
from . import _helpers

class _Chain(_Base):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Chain, self).__init__()
        self._name = "chain"
        self._residues = []

    def _add_residue(self, residue):
        self._residues.append(residue)
        residue._parent = self

    def _remove_residue(self, residue):
        self._residues.remove(residue)
        residue._parent = None
    
    def _set_residues(self, residues):
        self._residues = residues
        for residue in residues:
            residue._parent = self

    #region connections
    @property
    def _molecule(self):
        return self._parent

    @property
    def _complex(self):
        if self._parent:
            return self._parent._complex
        else:
            return None
    #endregion

    def _shallow_copy(self):
        chain = _Chain._create()
        chain._name = self._name
        return chain

    def _deep_copy(self):
        return _helpers._copy._deep_copy_chain(self)
