from nanome.util.color import Color
from . import UIBase
from nanome._internal._ui import _Image

class Image(_Image, UIBase):
    def __init__(self, file_path):
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

_Image._create = Image