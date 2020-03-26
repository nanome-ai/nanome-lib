from nanome.util import Vector3

class _UnitCell(object):
    def __init__(self):
        self._A = 0.0
        self._B = 0.0
        self._C = 0.0

        self._Alpha = 0.0
        self._Beta = 0.0
        self._Gamma = 0.0

        self._Origin = Vector3()
