__metaclass__ = type
#classes inherting from _UIBase are expected to also inherit UIBase separately.
class _UIBase(object):
    id_gen = 0
    def __init__(self):
        #protocol
        self._content_id = _UIBase.id_gen
        _UIBase.id_gen += 1

    def _copy_values_deep(self, other):
        pass

    def _clone(self):
        result = self.__class__()
        result._copy_values_deep(self)
        return result