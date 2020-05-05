from nanome.util.color import Color
from nanome._internal._ui import _DropdownItem

class DropdownItem(_DropdownItem):
    def __init__(self):
        # type: (_DropdownItem)
        _DropdownItem.__init__(self)

    @property
    def permanent_name(self):
        # type: () -> str
        return self._permanent_name
    @permanent_name.setter
    def permanent_name(self, value):
        # type: (str)
        self._permanent_name = value

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

_DropdownItem._create = DropdownItem