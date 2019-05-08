import math
#placeholder quaternion

class Quaternion(object):
    def __init__(self, x=0, y=0, z=0, w=0):
        self._x = float(x)
        self._y = float(y)
        self._z = float(z)
        self._w = float(w)
    
    def __str__(self):
        s = ' '.join([str(self._x), str(self._y), str(self._z), str(self._w)])
        return s

    def set(self, x, y, z, w):
        self._x = float(x)
        self._y = float(y)
        self._z = float(z)
        self._w = float(w)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def w(self):
        return self._w