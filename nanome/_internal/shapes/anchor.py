

class _Anchor(object):
    def __init__(self):
        from nanome.util import Vector3
        from nanome.util.enums import ShapeAnchorType
        self._target = 0
        self._local_offset = Vector3()
        self._global_offset = Vector3()
        self._viewer_offset = Vector3()
        self._anchor_type = ShapeAnchorType.Workspace

    @classmethod
    def _create(cls):
        return cls()
