import nanome
from . import UIBase
from nanome.util.color import Color
from nanome._internal._ui import _Image

class Image(_Image, UIBase):
    ScalingOptions = nanome.util.enums.ScalingOptions
    
    def __init__(self, file_path = ""):
        _Image.__init__(self)
        UIBase.__init__(self)
        self._file_path = file_path

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        self._color = value

    @property
    def file_path(self):
        return self._file_path
    
    @file_path.setter
    def file_path(self, value):
        self._file_path = value

    @property
    def scaling_option(self):
        return self._scaling_option
    
    @scaling_option.setter
    def scaling_option(self, value):
        self._scaling_option = value

    def register_pressed_callback(self, func):
        _Image._register_pressed_callback(self, func)

    def register_held_callback(self, func):
        _Image._register_held_callback(self, func)

    def register_released_callback(self, func):
        _Image._register_released_callback(self, func)
_Image._create = Image