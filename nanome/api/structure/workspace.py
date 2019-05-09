from nanome._internal._structure._workspace import _Workspace


class Workspace(_Workspace):
    def __init__(self):
        _Workspace.__init__(self)
        self.transform = self._transform

    @property
    def complexes(self):
        return self._complexes
    @complexes.setter
    def complexes(self, value):
        self._complexes = value

    class Transform(_Workspace.Transform):
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

        @property
        def scale(self):
            return self._scale
        @scale.setter
        def scale(self, value):
            self._scale = value

    _Workspace.Transform._create = Transform


_Workspace._create = Workspace
