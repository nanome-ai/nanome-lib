from nanome._internal._structure._chain import _Chain

class Chain(_Chain):
    def __init__(self):
        _Chain.__init__(self)
        self.molecular = self._molecular

    @property
    def residues(self):
        return self._residues
    @residues.setter
    def residues(self, value):
        self._residues = value

    class Molecular(_Chain.Molecular):
        @property
        def name(self):
            return self._name
        @name.setter
        def name(self, value):
            self._name = value
    _Chain.Molecular._create = Molecular

_Chain._create = Chain