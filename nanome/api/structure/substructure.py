import nanome
from nanome._internal._structure._substructure import _Substructure


class Substructure(_Substructure):
    SubstructureType = nanome.util.enums.SubstructureType

    def __init__(self):
        _Substructure.__init__(self)

    # region Generators
    @property
    def residues(self):
        """
        | The list of residues within this substructure
        """
        for atom in self._residues:
            yield atom

    @property
    def name(self):
        """
        | The name of the substructure

        :type: :class:`str`
        """
        return self._name

    @property
    def structure_type(self):
        """
        | 

        :type: :class:`~nanome.util.enums.SubstructureType`
        """
        return self._structure_type


_Substructure._create = Substructure
