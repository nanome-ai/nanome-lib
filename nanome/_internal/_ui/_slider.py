from . import _UIBase

class _Slider(_UIBase):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        #Protocol
        super(_Slider, self).__init__()
        self._current_value = 0.0
        self._min_value = 0.0
        self._max_value = 1.0
        #API
        self._changed_callback = lambda self: None
        self._released_callback = lambda self: None

    def _on_slider_changed (self):
        self._changed_callback(self)

    def _on_slider_released (self):
        self._released_callback(self)

    def _copy_values_deep(self, other):
        super(_Slider, self)._copy_values_deep(other)
        self._current_value = other._current_value
        self._min_value = other._min_value
        self._max_value = other._max_value