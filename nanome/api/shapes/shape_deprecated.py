from nanome._internal.decorators import deprecated
from . import Shape


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


Shape.target = target
Shape.anchor = anchor
Shape.position = position
