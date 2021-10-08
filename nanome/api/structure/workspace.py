from nanome._internal._structure._workspace import _Workspace
from nanome.util import Matrix, Logs
from .client import WorkspaceClient


class Workspace(_Workspace):
    """
    | Workspace that contains all the complexes shown in Nanome.
    """
    client = WorkspaceClient()

    def __init__(self):
        _Workspace.__init__(self)
        self._transform = Workspace.Transform(self)
        self.client = WorkspaceClient(self)

    @property
    def complexes(self):
        """
        | The list of complexes within the workspace

        :type: list of :class:`~nanome.structure.Complex`
        """
        return self._complexes

    @complexes.setter
    def complexes(self, value):
        self._complexes = value

    def add_complex(self, complex):
        """
        | Add complex to the workspace

        :param complex: Complex to add to the workspace
        :type complex: :class:`~nanome.structure.Complex`
        """
        complex.index = -1
        self._add_complex(complex)

    def remove_complex(self, complex):
        """
        | Remove complex from the workspace

        :param complex: Complex to remove from the workspace
        :type complex: :class:`~nanome.structure.Complex`
        """
        complex.index = -1
        self._remove_complex(complex)

    # region fields
    @property
    def position(self):
        """
        | Position of the workspace

        :type: :class:`~nanome.util.Vector3`
        """
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def rotation(self):
        """
        | Rotation of the workspace

        :type: :class:`~nanome.util.Quaternion`
        """
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value

    @property
    def scale(self):
        """
        | Scale of the workspace

        :type: :class:`~nanome.util.Vector3`
        """
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
    # endregion

    def get_workspace_to_world_matrix(self):
        return Matrix.compose_transformation_matrix(self._position, self._rotation, self._scale)

    def get_world_to_workspace_matrix(self):
        return self.get_workspace_to_world_matrix().get_inverse()

    # region deprecated
    @property
    @Logs.deprecated()
    def transform(self):
        return self._transform

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

        @property
        def scale(self):
            return self.parent.scale

        @scale.setter
        def scale(self, value):
            self.parent.scale = value

    # endregion
Workspace.client._setup_addon(Workspace)
_Workspace._create = Workspace
