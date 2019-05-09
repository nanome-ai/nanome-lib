import nanome
from nanome.util import Vector3
from nanome.util import IntEnum

class _Controller(object):
    _ControllerType = nanome.util.enums.ControllerType

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Controller, self).__init__()
        self._controller_type = _Controller._ControllerType.head
        self._position = Vector3(0,0,0)
        self._rotation = Vector3(0,0,0)
        self._thumb_padX = 0.0
        self._thumb_padY = 0.0
        self._trigger_position = False
        self._grip_position = False
        self._button1_pressed = False
        self._button2_pressed = False