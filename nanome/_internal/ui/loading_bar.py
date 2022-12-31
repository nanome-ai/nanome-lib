from . import _UIBase


class _LoadingBar(_UIBase):
    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_LoadingBar, self).__init__()
        self._percentage = 0.0
        self._title = ""
        self._description = ""
        self._failure = False

    def _copy_values_deep(self, other):
        super()._copy_values_deep(other)
        self._percentage = other._percentage
        self._title = other._title
        self._description = other._description
        self._failure = other._failure
