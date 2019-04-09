from . import _UIBase
from nanome.util import Color

class _Image(_UIBase):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Image, self).__init__()
        self._file_path = ""
        self._color = Color.White()
        
    def _copy_values_deep(self, other):
        super()._copy_values_deep(other)
        self._color = other._color
        self._file_path = other._file_path

