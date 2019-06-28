from nanome._internal._structure._complex import _Complex
from nanome.util import Matrix, Logs
from .io import ComplexIO
from . import Base


class Complex(_Complex, Base):
    io = ComplexIO()

    def __init__(self):
        super(Complex, self).__init__()
        self._rendering = Complex.Rendering(self)
        self._molecular = Complex.Molecular(self)
        self._transform = Complex.Transform(self)
        self.io = ComplexIO(self)

    def add_molecule(self, molecule):
        molecule.index = -1
        self._molecules.append(molecule)

    def remove_molecule(self, molecule):
        molecule.index = -1
        self._molecules.remove(molecule)

    #region Generators
    @property
    def molecules(self):
        for molecule in self._molecules:
            yield molecule

    @property
    def chains(self):
        for molecule in self.molecules:
            for chain in molecule.chains:
                yield chain

    @property
    def residues(self):
        for chain in self.chains:
            for residue in chain.residues:
                yield residue

    @property
    def atoms(self):
        for residue in self.residues:
            for atom in residue.atoms:
                yield atom

    @property
    def bonds(self):
        for residue in self.residues:
            for bond in residue.bonds:
                yield bond
    #endregion

    #region all fields
    @property
    def boxed(self):
        return self._boxed
    @boxed.setter
    def boxed(self, value):
        self._boxed = value

    @property
    def locked(self):
        return self._locked
    @locked.setter
    def locked(self, value):
        self._locked = value
        if (value):
            self._boxed = True

    @property
    def visible(self):
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
        return self._current_frame
    @current_frame.setter
    def current_frame(self, value):
        self._current_frame = value

    # returns true if the complex is selected on nanome.
    def get_selected(self):
        return self._selected

    def set_surface_needs_redraw(self):
        self._surface_dirty = True

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self._position = value

    @property
    def rotation(self):
        return self._rotation
    @rotation.setter
    def rotation(self, value):
        self._rotation = value

    def get_workspace_to_complex_matrix(self):
        rotation = Matrix.from_quaternion(self._rotation)
        rotation.transpose()

        translation = Matrix.identity(4)
        translation[0][3] = -self._position.x
        translation[1][3] = -self._position.y
        translation[2][3] = -self._position.z

        transformation = rotation * translation
        return transformation

    def get_complex_to_workspace_matrix(self):
        result = self.get_workspace_to_complex_matrix()
        result = result.get_inverse()
        return result
    #endregion

    #region depricated
    @property
    @Logs.deprecated()
    def rendering(self):
        return self._rendering

    @property
    @Logs.deprecated()
    def molecular(self):
        return self._molecular

    @property
    @Logs.deprecated()
    def transform(self):
        return self._transform

    class Rendering(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def boxed(self):
            return self.parent._boxed
        @boxed.setter
        def boxed(self, value):
            self.parent.boxed = value

        @property
        def locked(self):
            return self.parent.locked
        @locked.setter
        def locked(self, value):
            self.parent.locked = value
            if (value):
                self.parent.boxed = True

        @property
        def visible(self):
            return self.parent.visible
        @visible.setter
        def visible(self, value):
            self.parent.visible = value

        @property
        def computing(self):
            return self.parent.computing
        @computing.setter
        def computing(self, value):
            self.parent.computing = value

        @property
        def current_frame(self):
            return self.parent.current_frame
        @current_frame.setter
        def current_frame(self, value):
            self.parent.current_frame = value

        # returns true if the complex is selected on nanome.
        def get_selected(self):
            return self.parent.selected

        def set_surface_needs_redraw(self):
            self.parent.surface_dirty = True

    class Molecular(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def name(self):
            return self.parent.name
        @name.setter
        def name(self, value):
            self.parent.name = value

    class Transform(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def position(self):
            return self.parent.position
        @position.setter
        def position(self, value):
            self.parent.position = value

        @property
        def rotation(self):
            return self.parent.rotation
        @rotation.setter
        def rotation(self, value):
            self.parent.rotation = value

        def get_workspace_to_complex_matrix(self):
            rotation = Matrix.from_quaternion(self.parent.rotation)
            rotation.transpose()

            translation = Matrix.identity(4)
            translation[0][3] = -self.parent.position.x
            translation[1][3] = -self.parent.position.y
            translation[2][3] = -self.parent.position.z

            transformation = rotation * translation
            return transformation

        def get_complex_to_workspace_matrix(self):
            result = self.parent.get_workspace_to_complex_matrix()
            result = result.get_inverse()
            return result
    #endregion
Complex.io._setup_addon(Complex)
_Complex._create = Complex
