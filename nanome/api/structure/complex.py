from nanome._internal.structure.models import _Complex
from nanome._internal.network import PluginNetwork
from nanome._internal.enums import Messages
from nanome.util import Matrix, Logs
from .io import ComplexIO
from . import Base
from ._deprecated import ComplexDeprecated


class Complex(_Complex, ComplexDeprecated, Base):
    """
    | Represents a Complex that contains molecules.
    """
    io = ComplexIO()

    def __init__(self):
        super(Complex, self).__init__()
        self.io = ComplexIO(self)

    def add_molecule(self, molecule):
        """
        | Add a molecule to this complex

        :param molecule: Molecule to add to the chain
        :type molecule: :class:`~nanome.structure.Molecule`
        """
        molecule.index = -1
        self._add_molecule(molecule)

    def remove_molecule(self, molecule):
        """
        | Remove a molecule from this complex

        :param molecule: Molecule to remove from the chain
        :type molecule: :class:`~nanome.structure.Molecule`
        """
        molecule.index = -1
        self._remove_molecule(molecule)

    # region Generators
    @property
    def molecules(self):
        """
        | The list of molecules within this complex
        """
        for molecule in self._molecules:
            yield molecule

    @molecules.setter
    def molecules(self, molecule_list):
        self._molecules = molecule_list

    @property
    def chains(self):
        """
        | The list of chains within this complex
        """
        for molecule in self.molecules:
            for chain in molecule.chains:
                yield chain

    @property
    def residues(self):
        """
        | The list of residues within this complex
        """
        for chain in self.chains:
            for residue in chain.residues:
                yield residue

    @property
    def atoms(self):
        """
        | The list of atoms within this complex
        """
        for residue in self.residues:
            for atom in residue.atoms:
                yield atom

    @property
    def bonds(self):
        """
        | The list of bonds within this complex
        """
        for residue in self.residues:
            for bond in residue.bonds:
                yield bond
    # endregion

    # region all fields
    @property
    def boxed(self):
        """
        | Represents if this complex is boxed/bordered in Nanome.

        :type: :class:`bool`
        """
        return self._boxed

    @boxed.setter
    def boxed(self, value):
        self._boxed = value

    @property
    def locked(self):
        """
        | Represents if this complex is locked and unmovable in Nanome.

        :type: :class:`bool`
        """
        return self._locked

    @locked.setter
    def locked(self, value):
        self._locked = value

    @property
    def visible(self):
        """
        | Represents if this complex is visible in Nanome.

        :type: :class:`bool`
        """
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def computing(self):
        return self._computing

    @computing.setter
    def computing(self, value):
        self._computing = value

    @property
    def current_frame(self):
        """
        | Represents the current animation frame the complex is in.

        :type: :class:`int`
        """
        return self._current_frame

    @current_frame.setter
    def current_frame(self, value):
        value = max(0, min(value, len(self._molecules) - 1))
        self._current_frame = value

    def set_current_frame(self, value):
        self.current_frame = value

    # returns true if the complex is selected on nanome.
    def get_selected(self):
        return self._selected

    def get_all_selected(self):
        for atom in self.atoms:
            if not atom.selected:
                return False
        return True

    def set_all_selected(self, value):
        for atom in self.atoms:
            atom.selected = value

    def set_surface_needs_redraw(self):
        self._surface_dirty = True

    @property
    def box_label(self):
        """
        | Represents the label on the box surrounding the complex

        :type: :class:`str`
        """
        return self._box_label

    @box_label.setter
    def box_label(self, value):
        self._box_label = value

    @property
    def name(self):
        """
        | Represents the name of the complex

        :type: :class:`str`
        """
        return self._name

    @name.setter
    def name(self, value):
        if type(value) is not str:
            value = str(value)
        self._name = value

    @property
    def index_tag(self):
        return self._index_tag

    @index_tag.setter
    def index_tag(self, value):
        self._index_tag = value

    @property
    def split_tag(self):
        return self._split_tag

    @split_tag.setter
    def split_tag(self, value):
        self._split_tag = value

    @property
    def full_name(self):
        """
        | Represents the full name of the complex with its tags and name

        :type: :class:`str`
        """
        fullname = self._name
        has_tag = False

        if self._index_tag > 0:
            fullname = fullname + " {" + str(self._index_tag)
            has_tag = True

        if self._split_tag is not None and len(self._split_tag) > 0:
            if has_tag:
                fullname = fullname + "-" + self._split_tag
            else:
                fullname = fullname + " {" + self._split_tag
            has_tag = True

        if has_tag:
            fullname = fullname + "}"

        return fullname

    @full_name.setter
    def full_name(self, value):
        self._name = value
        self._index_tag = 0
        self._split_tag = ''

    @property
    def position(self):
        """
        | Position of the complex

        :type: :class:`~nanome.util.Vector3`
        """
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def rotation(self):
        """
        | Rotation of the complex

        :type: :class:`~nanome.util.Quaternion`
        """
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value

    @property
    def remarks(self):
        """
        | remarks section of the complex file

        :type: :class: dict
        """
        return self._remarks

    @remarks.setter
    def remarks(self, value):
        self._remarks = value

    def get_workspace_to_complex_matrix(self):
        return self.get_complex_to_workspace_matrix().get_inverse()

    def get_complex_to_workspace_matrix(self):
        return Matrix.compose_transformation_matrix(self._position, self._rotation)
    # endregion

    def convert_to_conformers(self, force_conformers=None):
        return self._convert_to_conformers(force_conformers)

    def convert_to_frames(self):
        return self._convert_to_frames()

    def register_complex_updated_callback(self, callback):
        from nanome.api import PluginInstance
        self._complex_updated_callback = callback
        PluginInstance._hook_complex_updated(self.index, callback)
        PluginNetwork.send(Messages.hook_complex_updated, self.index, False)

    def register_selection_changed_callback(self, callback):
        from nanome.api import PluginInstance
        self._selection_changed_callback = callback
        PluginInstance._hook_selection_changed(self.index, callback)
        PluginNetwork.send(Messages.hook_selection_changed, self.index, False)

    @staticmethod
    def align_origins(target_complex, *other_complexes):
        for complex in other_complexes:
            complex.position = target_complex.position.get_copy()
            complex.rotation = target_complex.rotation.get_copy()


Complex.io._setup_addon(Complex)
_Complex._create = Complex
