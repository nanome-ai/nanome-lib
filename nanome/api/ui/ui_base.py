import os
#classes inherting from UIBase are expected to also inherit _UIBase separately.
class UIBase(object):
    def __init__(self, name = "default"):
        # type: (str)
        self._name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value

    def clone(self):
        return self._clone()
        