from . import UIBase
from nanome._internal._ui import _Slider


class Slider(_Slider, UIBase):
    """
    | Represents a slider that has a set range of values
    """

    def __init__(self, min_val=None, max_val=None, current_val=None):
        _Slider.__init__(self)
        UIBase.__init__(self)
        if min_val is not None:
            self.min_value = min_val
        if max_val is not None:
            self.max_value = max_val
        if current_val is not None:
            self.current_value = current_val

    @property
    def current_value(self):
        """
        | The current value of the slider

        :type: :class:`float`
        """
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        self._current_value = value

    @property
    def min_value(self):
        """
        | The minimum (far left) value of the slider

        :type: :class:`float`
        """
        return self._min_value

    @min_value.setter
    def min_value(self, value):
        self._min_value = value

    @property
    def max_value(self):
        """
        | The minimum (far right) value of the slider

        :type: :class:`float`
        """
        return self._max_value

    @max_value.setter
    def max_value(self, value):
        self._max_value = value

    def register_changed_callback(self, func):
        """
        | Register a function to be called every time the value of the slider changes

        :param func: callback function to execute when slider changes values
        :type func: method (:class:`~nanome.ui.Slider`) -> None
        """
        self._changed_callback = func

    def register_released_callback(self, func):
        """
        | Register a function to be called when the slider is released.

        :param func: callback function to execute when slider is released
        :type func: method (:class:`~nanome.ui.Slider`) -> None
        """
        self._released_callback = func


_Slider._create = Slider
