from nanome.util.color import Color
from nanome._internal._ui import _DropdownItem

class DropdownItem(_DropdownItem):
    def __init__(self, name = "item"):
        # type: (_DropdownItem)
        _DropdownItem.__init__(self)
        self.name = name

    @property
    def name(self):
        # type: () -> str
        return self._name
    @name.setter
    def name(self, value):
        # type: (str)
        self._name = value

    @property
    def close_on_selected(self):
        # type: () -> bool
        return self._close_on_selected
    @close_on_selected.setter
    def close_on_selected(self, value):
        # type: (bool)
        self._close_on_selected = value

    @property
    def selected(self):
        # type: () -> bool
        return self._selected
    @selected.setter
    def selected(self, value):
        # type: (bool)
        self._selected = value

    def clone(self):
        # type: (_DropdownItem)
        return self._clone()

_DropdownItem._create = DropdownItem
