
class _DropdownItem():
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_DropdownItem, self).__init__()
        self._name = ""
        self._close_on_selected = True
        self._selected = False

    def _copy_values_deep(self, other):
        self._name = other._name
        self._close_on_selected = other._close_on_selected
        self._selected = other._selected

    def _clone(self):
        other = _DropdownItem._create()
        other._copy_values_deep(self)
        return other
