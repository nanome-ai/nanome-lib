from . import _UIBase

class _Dropdown(_UIBase):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Dropdown, self).__init__()
        self._permanent_title = ""
        self._use_permanent_title = False
        self._max_displayed_items = 5
        self._items = []
        
    def _copy_values_deep(self, other):
        super(_Dropdown, self)._copy_values_deep(other)
        self._permanent_title = other._permanent_title
        self._use_permanent_title = other._use_permanent_title
        self._max_displayed_items = other._max_displayed_items
        self._items = [item._clone() for item in other._items]
