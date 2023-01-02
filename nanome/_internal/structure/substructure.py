
class _Substructure:

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        self._name = ''
        self._residues = []
        self._structure_type = None

    @property
    def SubstructureType(self):
        from nanome.util import enums
        return enums.SubstructureType