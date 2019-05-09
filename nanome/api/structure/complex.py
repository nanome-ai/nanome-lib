from nanome._internal._structure._complex import _Complex
from nanome.util import Matrix
from .io import ComplexIO
from . import Base


class Complex(_Complex, Base):
    io = ComplexIO()

    def __init__(self):
        super(Complex, self).__init__()
        self.rendering = self._rendering
        self.molecular = self._molecular
        self.transform = self._transform
        self.io = ComplexIO(self)

    def add_molecule(self, molecule):
        self._molecules.append(molecule)

    def remove_molecule(self, molecule):
        self._molecules.remove(molecule)

    class Rendering(_Complex.Rendering):
        @property
        def boxed(self):
            return self._boxed
        @boxed.setter
        def boxed(self, value):
            self._boxed = value

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
    _Complex.Rendering._create = Rendering

    class Molecular(_Complex.Molecular):
        @property
        def name(self):
            return self._name
        @name.setter
        def name(self, value):
            self._name = value
    _Complex.Molecular._create = Molecular

    class Transform(_Complex.Transform):
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

    _Complex.Transform._create = Transform

    #Generators:
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


Complex.io._setup_addon(Complex)
_Complex._create = Complex
