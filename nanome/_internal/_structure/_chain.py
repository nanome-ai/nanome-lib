from . import _Base

class _Chain(_Base):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Chain, self).__init__()
        self._name = "chain"
        self._residues = []