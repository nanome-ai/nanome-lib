from nanome._internal._structure._chain import _Chain
from nanome.util import Logs
from . import Base


class Chain(_Chain, Base):
    """
    | Represents a Chain. Contains residues. Molecules contains chains.
    """

    def __init__(self):
        super(Chain, self).__init__()
        self._molecular = Chain.Molecular(self)

    def add_residue(self, residue):
        """
        | Add a residue to this chain

        :param residue: Residue to add to the chain
        :type residue: :class:`~nanome.structure.Residue`
        """
        residue.index = -1
        self._add_residue(residue)

    def remove_residue(self, residue):
        """
        | Remove a residue from this chain

        :param residue: Residue to remove from the chain
        :type residue: :class:`~nanome.structure.Residue`
        """
        residue.index = -1
        self._remove_residue(residue)

    # region Generators:
    @property
    def residues(self):
        """
        | The list of residues that this chain contains
        """
        for residue in self._residues:
            yield residue

    @residues.setter
    def residues(self, residue_list):
        self._residues = residue_list

    @property
    def atoms(self):
        """
        | The list of atoms that this chain's residues contain
        """
        for residue in self.residues:
            for atom in residue.atoms:
                yield atom

    @property
    def bonds(self):
        """
        | The list of bonds within this chain
        """
        for residue in self.residues:
            for bond in residue.bonds:
                yield bond
    # endregion

    # region connections
    @property
    def molecule(self):
        """
        | Molecule that this chain is in
        """
        return self._molecule

    @property
    def complex(self):
        """
        | Complex that this chain is in
        """
        return self._complex
    # endregion

    # region all fields
    @property
    def name(self):
        """
        | Represents the name of the chain

        :type: :class:`str`
        """
        return self._name

    @name.setter
    def name(self, value):
        if type(value) is not str:
            value = str(value)
        self._name = value
    # endregion

    # region deprecated
    @property
    @Logs.deprecated()
    def molecular(self):
        return self._molecular

    class Molecular(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def name(self):
            return self.parent.name

        @name.setter
        def name(self, value):
            self.parent.name = value

    # endregion
_Chain._create = Chain
