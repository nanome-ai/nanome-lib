from . import _UIBase


class _UIList(_UIBase):

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_UIList, self).__init__()
        self._items = []
        self._display_columns = 1
        self._display_rows = 10
        self._total_columns = 1
        self._unusable = False

    def _copy_values_deep(self, other):
        super(_UIList, self)._copy_values_deep(other)
        self._items = []
        for item in other._items:
            self._items.append(item.clone())
        self._display_columns = other._display_columns
        self._display_rows = other._display_rows
        self._total_columns = other._total_columns
        self._unusable = other._unusable
