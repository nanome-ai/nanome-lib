import nanome
from nanome._internal._structure._atom import _Atom
from nanome.util import Logs
from . import Base


class Atom(_Atom, Base):
    """
    | Represents an Atom
    """
    AtomRenderingMode = nanome.util.enums.AtomRenderingMode

    def __init__(self):
        super(Atom, self).__init__()
        self._rendering = Atom.Rendering(self)
        self._molecular = Atom.Molecular(self)

    # region connections
    @property
    def bonds(self):
        """
        | Bonds that the atom is part of
        """
        for bond in self._bonds:
            yield bond

    @property
    def residue(self):
        """
        | Residue that the atom is part of
        """
        return self._residue

    @property
    def chain(self):
        """
        | Chain that the atom is part of
        """
        return self._chain

    @property
    def molecule(self):
        """
        | Molecule that the atom is part of
        """
        return self._molecule

    @property
    def complex(self):
        """
        | Complex that the atom is part of
        """
        return self._complex
    # endregion

    # region all fields
    def set_visible(self, value):
        """
        | Set the atom to be visible or invisible in Nanome.

        :type: :class:`bool`
        """
        if value:
            self._display_mode = 0xFFFFFFFF
        else:
            self._display_mode = 0x00000000
        self._hydrogened = value
        self._watered = value
        self._hetatomed = value

    @property
    def selected(self):
        """
        | Represents if the atom is currently selected in the Nanome workspace.

        :type: :class:`bool`
        """
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

    @property
    def atom_mode(self):
        """
        | Represents how the atom should be shown, such as ball and point or wired.

        :type: :class:`~nanome.util.enums.AtomRenderingMode`
        """
        return self._atom_mode

    @atom_mode.setter
    def atom_mode(self, value):
        self._atom_mode = value

    @property
    def labeled(self):
        """
        | Represents if the atom has a label or not. If it does, show the label.

        :type: :class:`bool`
        """
        return self._labeled

    @labeled.setter
    def labeled(self, value):
        self._labeled = value

    @property
    def label_text(self):
        """
        | Represents the text that would show up if atom is labeled.

        :type: :class:`str`
        """
        return self._label_text

    @label_text.setter
    def label_text(self, value):
        if type(value) is not str:
            value = str(value)
        self._label_text = value

    @property
    def atom_rendering(self):
        """
        | Represents if the atom should be rendered specifically.

        :type: :class:`bool`
        """
        return self._atom_rendering

    @atom_rendering.setter
    def atom_rendering(self, value):
        self._atom_rendering = value

    @property
    def atom_color(self):
        """
        | Color of the atom

        :type: :class:`~nanome.util.Color`
        """
        return self._atom_color

    @atom_color.setter
    def atom_color(self, value):
        self._atom_color = value

    @property
    def atom_scale(self):
        """
        | Scale/size/radius of the atom

        :type: :class:`float`
        """
        return self._atom_scale

    @atom_scale.setter
    def atom_scale(self, value):
        self._atom_scale = value

    @property
    def surface_rendering(self):
        """
        | Represents if the atom surface should be rendered specifically.

        :type: :class:`bool`
        """
        return self._surface_rendering

    @surface_rendering.setter
    def surface_rendering(self, value):
        self._surface_rendering = value

    @property
    def surface_color(self):
        """
        | Color of the atom surface

        :type: :class:`~nanome.util.Color`
        """
        return self._surface_color

    @surface_color.setter
    def surface_color(self, value):
        self._surface_color = value

    @property
    def surface_opacity(self):
        """
        | Opacity of the atom surface

        :type: :class:`float`
        """
        return self._surface_opacity

    @surface_opacity.setter
    def surface_opacity(self, value):
        self._surface_opacity = value

    @property
    def symbol(self):
        """
        | Represents the symbol of the atom. E.g.: C for Carbon

        :type: :class:`str`
        """
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        if type(value) is not str:
            value = str(value)
        self._symbol = value

    @property
    def serial(self):
        return self._serial

    @serial.setter
    def serial(self, value):
        self._serial = value

    @property
    def name(self):
        """
        | Represents the name of the atom. Ideally, the same as symbol.

        :type: :class:`str`
        """
        return self._name

    @name.setter
    def name(self, value):
        if type(value) is not str:
            value = str(value)
        self._name = value

    @property
    def position(self):
        """
        | Position of the atom

        :type: :class:`~nanome.util.Vector3`
        """
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def exists(self):
        """
        | Represents if atom exists for calculations.

        :type: :class:`bool`
        """
        return self._exists

    @exists.setter
    def exists(self, value):
        self._exists = value

    @property
    def is_het(self):
        """
        | Represents if the atom is a HET (Heteroatom - not C or H).

        :type: :class:`bool`
        """
        return self._is_het

    @is_het.setter
    def is_het(self, value):
        self._is_het = value

    @property
    def formal_charge(self):
        return self._formal_charge

    @formal_charge.setter
    def formal_charge(self, value):
        self._formal_charge = value

    @property
    def partial_charge(self):
        return self._partial_charge

    @partial_charge.setter
    def partial_charge(self, value):
        self._partial_charge = value

    @property
    def occupancy(self):
        return self._occupancy

    @occupancy.setter
    def occupancy(self, value):
        self._occupancy = value

    @property
    def bfactor(self):
        return self._bfactor

    @bfactor.setter
    def bfactor(self, value):
        self._bfactor = value

    @property
    def acceptor(self):
        return self._acceptor

    @acceptor.setter
    def acceptor(self, value):
        self._acceptor = value

    @property
    def donor(self):
        return self._donor

    @donor.setter
    def donor(self, value):
        self._donor = value

    @property
    def polar_hydrogen(self):
        return self._polar_hydrogen

    @polar_hydrogen.setter
    def polar_hydrogen(self, value):
        self._polar_hydrogen = value

    @property
    def vdw_radius(self):
        """
        | VDW radius of the atom in Angstrom

        :type: :class:`float`
        """
        return self._vdw_radius

    @vdw_radius.setter
    def vdw_radius(self, value):
        self._vdw_radius = value

    @property
    def alt_loc(self):
        """
        | String of length 1. Identifier of the alternate location.

        :type: :class:`str`
        """
        return self._alt_loc

    @alt_loc.setter
    def alt_loc(self, value):
        self._alt_loc = value[0]
    # endregion

    # region conformer stuff
    @property
    def current_conformer(self):
        return self._current_conformer

    @property
    def conformer_count(self):
        return self._conformer_count

    @property
    def positions(self):
        return self._positions

    @positions.setter
    def positions(self, value):
        if self.molecule is not None:
            if len(value) != self.conformer_count:
                raise ValueError("Length of positions must match the conformer count of the parent molecule.")
        self._positions = value

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
    def rendering(self):
        return self._rendering

    @property
    @Logs.deprecated()
    def molecular(self):
        return self._molecular

    class Rendering(object):
        def __init__(self, parent):
            self._parent = parent

        def set_visible(self, value):
            if value:
                self._parent._display_mode = 0xFFFFFFFF
            else:
                self._parent._display_mode = 0x00000000
            self._parent._hydrogened = value
            self._parent._watered = value
            self._parent._hetatomed = value

        @property
        def selected(self):
            return self._parent.selected

        @selected.setter
        def selected(self, value):
            self._parent.selected = value

        @property
        def atom_mode(self):
            return self._parent.atom_mode

        @atom_mode.setter
        def atom_mode(self, value):
            self._parent.atom_mode = value

        @property
        def labeled(self):
            return self._parent.labeled

        @labeled.setter
        def labeled(self, value):
            self._parent.labeled = value

        @property
        def label_text(self):
            return self._parent.label_text

        @label_text.setter
        def label_text(self, value):
            self._parent.label_text = value

        @property
        def atom_rendering(self):
            return self._parent.atom_rendering

        @atom_rendering.setter
        def atom_rendering(self, value):
            self._parent.atom_rendering = value

        @property
        def atom_color(self):
            return self._parent.atom_color

        @atom_color.setter
        def atom_color(self, value):
            self._parent.atom_color = value

        @property
        def surface_rendering(self):
            return self._parent.surface_rendering

        @surface_rendering.setter
        def surface_rendering(self, value):
            self._parent.surface_rendering = value

        @property
        def surface_color(self):
            return self._parent.surface_color

        @surface_color.setter
        def surface_color(self, value):
            self._parent.surface_color = value

        @property
        def surface_opacity(self):
            return self._parent.surface_opacity

        @surface_opacity.setter
        def surface_opacity(self, value):
            self._parent.surface_opacity = value

    class Molecular(object):
        def __init__(self, parent):
            self._parent = parent

        @property
        def symbol(self):
            return self._parent.symbol

        @symbol.setter
        def symbol(self, value):
            self._parent.symbol = value

        @property
        def serial(self):
            return self._parent.serial

        @serial.setter
        def serial(self, value):
            self._parent.serial = value

        @property
        def name(self):
            return self._parent.name

        @name.setter
        def name(self, value):
            self._parent.name = value

        @property
        def position(self):
            return self._parent.position

        @position.setter
        def position(self, value):
            self._parent.position = value

        @property
        def is_het(self):
            return self._parent.is_het

        @is_het.setter
        def is_het(self, value):
            self._parent.is_het = value

    # endregion
_Atom._create = Atom
