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