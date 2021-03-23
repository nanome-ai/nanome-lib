import nanome
from .. import _Shape

@property
@nanome.util.Logs.deprecated()
def target(self):
    return self._anchors[0].target
@target.setter
@nanome.util.Logs.deprecated()
def target(self, value):
    self._anchors[0].target = value

@property
@nanome.util.Logs.deprecated()
def anchor(self):
    return self._anchors[0].anchor_type
@anchor.setter
@nanome.util.Logs.deprecated()
def anchor(self, value):
    self._anchors[0].anchor_type = value

@property
@nanome.util.Logs.deprecated()
def position(self):
    return self._anchors[0].local_offset
@position.setter
@nanome.util.Logs.deprecated()
def position(self, value):
    self._anchors[0].local_offset = value

_Shape.target = target
_Shape.anchor = anchor
_Shape.position = position