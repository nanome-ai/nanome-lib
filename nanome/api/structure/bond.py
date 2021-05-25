import nanome
from nanome.util import Logs
from nanome._internal._structure._bond import _Bond
from . import Base


class Bond(_Bond, Base):
    """
    | Represents a Bond between two atoms
    """
    Kind = nanome.util.enums.Kind

    def __init__(self):
        super(Bond, self).__init__()
        self._molecular = Bond.Molecular(self)

    # region connections
    @property
    def atom1(self):
        """
        First atom linked by this bond

        :type: :class:`~nanome.structure.Atom`
        """
        return self._atom1

    @atom1.setter
    def atom1(self, value):
        self._atom1 = value

    @property
    def atom2(self):
        """
        Second atom linked by this bond

        :type: :class:`~nanome.structure.Atom`
        """
        return self._atom2

    @atom2.setter
    def atom2(self, value):
        self._atom2 = value

    @property
    def residue(self):
        """
        | Residue that the bond is part of
        """
        return self._residue

    @property
    def chain(self):
        """
        | Chain that the bond is part of
        """
        return self._chain

    @property
    def molecule(self):
        """
        | Molecule that the bond is part of
        """
        return self._molecule

    @property
    def complex(self):
        """
        | Complex that the bond is part of
        """
        return self._complex
    # endregion

    # region all fields
    @property
    def kind(self):
        """
        | Kind of bond

        :type: :class:`~nanome.util.enums.Kind`
        """
        return self._kind

    @kind.setter
    def kind(self, value):
        self._kind = value

    @property
    def exists(self):
        """
        | Represents if bond exists for calculations.

        :type: :class:`bool`
        """
        return self._exists

    @exists.setter
    def exists(self, value):
        self._exists = value
    # endregion

    # region conformer stuff
    @property
    def current_conformer(self):
        return self._current_conformer

    @property
    def conformer_count(self):
        return self._conformer_count

    @property
    def kinds(self):
        return self._kinds

    @kinds.setter
    def kinds(self, value):
        if self.molecule is not None:
            if len(value) != self.conformer_count:
                raise ValueError("Length of kinds must match the conformer count of the parent molecule.")
        self._kinds = value

    @property
    def in_conformer(self):
        return self._in_conformer

    @in_conformer.setter
    def in_conformer(self, value):
        if self.molecule is not None:
            if len(value) != self.conformer_count:
                raise ValueError("Length of in_conformer must match the conformer count of the parent molecule.")
        self._in_conformer = value
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
        def kind(self):
            return self.parent.kind

        @kind.setter
        def kind(self, value):
            self.parent.kind = value

    # endregion
_Bond._create = Bond
