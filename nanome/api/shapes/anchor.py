from nanome._internal._shapes._anchor import _Anchor

class Anchor(_Anchor):
    def __init__(self):
        _Anchor.__init__(self)

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
    def anchor_type(self):
        return self._anchor_type

    @anchor_type.setter
    def anchor_type(self, value):
        self._anchor_type = value
_Anchor._create = Anchor