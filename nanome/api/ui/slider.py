from . import UIBase
from nanome._internal._ui import _Slider

class Slider(_Slider, UIBase):
    def __init__(self,  
                 min_val     = None, 
                 max_val     = None, 
                 current_val = None):
        # type: (str, float, float, float)
        _Slider.__init__(self)
        UIBase.__init__(self)
        if min_val != None:
            self.min_value = min_val
        if max_val != None:
            self.max_value = max_val
        if current_val != None:
            self.current_value = current_val

    @property
    def current_value(self):
        # type: () -> float
        return self._current_value
    @current_value.setter
    def current_value(self, value):
        # type: (float)
        self._current_value = value

    @property
    def min_value(self):
        # type: () -> float
        return self._min_value
    @min_value.setter
    def min_value(self, value):
        # type: (float)
        self._min_value = value

    @property
    def max_value(self):
        # type: () -> float
        return self._max_value
    @max_value.setter
    def max_value(self, value):
        # type: (float)
        self._max_value = value

    def register_changed_callback(self, func):
        self._changed_callback = func
    
    def register_released_callback(self, func):
        self._released_callback = func

_Slider._create = Slider