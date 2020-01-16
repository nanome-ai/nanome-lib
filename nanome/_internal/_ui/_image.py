import nanome
from . import _UIBase
from nanome.util import Color

class _Image(_UIBase):
    ScalingOptions = nanome.util.enums.ScalingOptions
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Image, self).__init__()
        self._file_path = ""
        self._color = Color.White()
        self._scaling_option = _Image.ScalingOptions.stretch
        self._pressed_callback = lambda self, x, y: None
        self._held_callback = lambda self, x, y: None
        self._released_callback = lambda self, x, y: None

    def _on_image_pressed (self, x, y):
        self._pressed_callback(self, x, y)

    def _on_image_held (self, x, y):
        self._held_callback(self, x, y)

    def _on_image_released (self, x, y):
        self._released_callback(self, x, y)

    def _register_pressed_callback(self, func):
        self._pressed_callback = func

    def _register_held_callback(self, func):
        self._held_callback = func

    def _register_released_callback(self, func):
        self._released_callback = func

    def _copy_values_deep(self, other):
        super()._copy_values_deep(other)
        self._color = other._color
        self._scaling_option = other._scaling_option
        self._file_path = other._file_path
        self._pressed_callback = other._pressed_callback
        self._held_callback = other._held_callback
        self._released_callback = other._released_callback
