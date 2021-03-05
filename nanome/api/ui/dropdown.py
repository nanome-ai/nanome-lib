from . import UIBase
from nanome._internal._ui import _Dropdown

class Dropdown(_Dropdown, UIBase):
    def __init__(self):
        # type: (_Dropdown)
        _Dropdown.__init__(self)
        UIBase.__init__(self)

    @property
    def permanent_title(self):
        # type: () -> str
        return self._permanent_title
    @permanent_title.setter
    def permanent_title(self, value):
        # type: (str)
        self._permanent_title = value

    @property
    def use_permanent_title(self):
        # type: () -> bool
        return self._use_permanent_title
    @use_permanent_title.setter
    def use_permanent_title(self, value):
        # type: (bool)
        self._use_permanent_title = value

    @property
    def max_displayed_items(self):
        # type: () -> int
        return self._max_displayed_items
    @max_displayed_items.setter
    def max_displayed_items(self, value):
        # type: (int)
        self._max_displayed_items = value

    @property
    def items(self):
        return self._items
    @items.setter
    def items(self, value):
        self._items = value

    def register_item_clicked_callback(self, func):
        _Dropdown._register_item_clicked_callback(self, func)

_Dropdown._create = Dropdown