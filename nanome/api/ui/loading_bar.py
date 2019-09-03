from nanome.util.color import Color
from . import UIBase
from nanome._internal._ui import _LoadingBar

class LoadingBar(_LoadingBar, UIBase):
    def __init__(self):
        _LoadingBar.__init__(self)
        UIBase.__init__(self)

    @property
    def percentage(self):
        return self._percentage
    
    @percentage.setter
    def percentage(self, value):
        self._percentage = value

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if type(value) is not str:
            value = str(value)
        self._title = value

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if type(value) is not str:
            value = str(value)
        self._description = value

    @property
    def failure(self):
        return self._failure
    
    @failure.setter
    def failure(self, value):
        self._failure = value

_LoadingBar._create = LoadingBar