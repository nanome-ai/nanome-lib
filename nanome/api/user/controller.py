import nanome
from nanome._internal._user._controller import _Controller
from nanome.util import Vector3
from nanome.util import IntEnum
class Controller(_Controller):

    ControllerType = nanome.util.enums.ControllerType

    def __init__(self):
        super(Controller, self).__init__()

    @property
    def controller_type(self):
        return self._controller_type

    @property
    def position(self):
        return self._position

    @property
    def rotation(self):
        return self._rotation

    @property
    def thumb_padX(self):
        return self._thumb_padX

    @property
    def thumb_padY(self):
        return self._thumb_padY

    @property
    def trigger_position(self):
        return self._trigger_position

    @property
    def grip_position(self):
        return self._grip_position

    @property
    def button1_pressed(self):
        return self._button1_pressed

    @property
    def button2_pressed(self):
        return self._button2_pressed

_Controller._create = Controller