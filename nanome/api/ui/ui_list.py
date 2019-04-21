from nanome._internal._ui import _UIList
from . import UIBase

class UIList(_UIList, UIBase):
    def __init__(self):
        # type: (str)
        _UIList.__init__(self)
        UIBase.__init__(self)

    @property
    def items(self):
        return self._items
    @items.setter
    def items(self, value):
        self._items = value

    @property
    def display_columns(self):
        # type: () -> int
        return self._display_columns
    @display_columns.setter
    def display_columns(self, value):
        # type: (int)
        self._display_columns = value

    @property
    def display_rows(self):
        # type: () -> int
        return self._display_rows
    @display_rows.setter
    def display_rows(self, value):
        # type: (int)
        self._display_rows = value
        
    @property
    def total_columns(self):
        # type: () -> int
        return self._total_columns
    @total_columns.setter
    def total_columns(self, value):
        # type: (int)
        self._total_columns = value
    
    @property
    def unusable(self):
        # type: () -> bool
        return self._unusable
    @unusable.setter
    def unusable(self, value):
        # type: (bool)
        self._unusable = value

_UIList._create = UIList