# classes inherting from UIBase are expected to also inherit _UIBase separately.


class UIBase(object):
    def __init__(self):
        pass

    def clone(self):
        return self._clone()
