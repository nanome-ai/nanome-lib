from nanome.util import Vector3
from nanome.util.enums import ShapeAnchorType


class Anchor:

    def __init__(self):
        self._target = 0
        self._local_offset = Vector3()
        self._global_offset = Vector3()
        self._viewer_offset = Vector3()
        self._anchor_type = ShapeAnchorType.Workspace

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def local_offset(self):
        return self._local_offset

    @local_offset.setter
    def local_offset(self, value):
        self._local_offset = value

    @property
    def global_offset(self):
        return self._global_offset

    @global_offset.setter
    def global_offset(self, value):
        self._global_offset = value

    @property
    def viewer_offset(self):
        return self._viewer_offset

    @viewer_offset.setter
    def viewer_offset(self, value):
        self._viewer_offset = value

    @property
    def anchor_type(self):
        return self._anchor_type

    @anchor_type.setter
    def anchor_type(self, value):
        self._anchor_type = value
