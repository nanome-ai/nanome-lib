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
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def anchor_type(self):
        return self._anchor_type

    @anchor_type.setter
    def anchor_type(self, value):
        self._anchor_type = value
_Anchor._create = Anchor