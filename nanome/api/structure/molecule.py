from nanome._internal._structure._molecule import _Molecule


class Molecule(_Molecule):
    def __init__(self):
        _Molecule.__init__(self)
        self.molecular = self._molecular
        
    @property
    def chains(self):
        return self._chains
    
    @chains.setter
    def chains(self, value):
        self._chains = value
        
    class Molecular(_Molecule.Molecular):
        @property
        def name(self):
            return self._name
        @name.setter
        def name(self, value):
            self._name = value
    _Molecule.Molecular._create = Molecular
_Molecule._create = Molecule