import nanome


class _Substructure:
    SubstructureType = nanome.util.enums.SubstructureType

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        self._name = ''
        self._residues = []
        self._structure_type = None
