import nanome
from .. import _Shape
from nanome._internal.util.decorators import deprecated


@property
@deprecated()
def target(self):
    return self._anchors[0].target


@target.setter
@deprecated()
def target(self, value):
    self._anchors[0].target = value


@property
@deprecated()
def anchor(self):
    return self._anchors[0].anchor_type


@anchor.setter
@deprecated()
def anchor(self, value):
    self._anchors[0].anchor_type = value


@property
@deprecated()
def position(self):
    return self._anchors[0].local_offset


@position.setter
@deprecated()
def position(self, value):
    self._anchors[0].local_offset = value


_Shape.target = target
_Shape.anchor = anchor
_Shape.position = position
