import math

class Vector3(object):
    def __init__(self, x=0, y=0, z=0):
        self._positions = [float(x), float(y), float(z)]

    def __getitem__(self, i):
        return self._positions[i]

    def __setitem__(self, i, value):
        self._positions[i] = float(value)

    def __str__(self):
        s = ' '.join([str(self._positions[0]), str(self._positions[1]), str(self._positions[2])])
        return s

    def get_copy(self):
        return Vector3(self._positions[0], self._positions[1], self._positions[2])

    @classmethod
    def distance(cls, v1, v2):
        return math.sqrt((v2.x - v1.x) ** 2 + (v2.y - v1.y) ** 2 + (v2.z - v1.z) ** 2)

    def __add__(self, other):
        return Vector3(self._positions[0] + other.x, self._positions[1] + other.y, self._positions[2] + other.z)

    def __sub__(self, other):
        return Vector3(self._positions[0] - other.x, self._positions[1] - other.y, self._positions[2] - other.z)

    def __mul__(self, scalar):
        return Vector3(self._positions[0] * scalar, self._positions[1] * scalar, self._positions[2] * scalar)

    def equals(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def unpack(self):
        return self._positions[0], self._positions[1], self._positions[2]

    def set(self, x, y, z):
        self._positions[0] = x
        self._positions[1] = y
        self._positions[2] = z

    @property
    def x(self):
        return self._positions[0]
    @x.setter
    def x(self, value):
        self._positions[0] = float(value)

    @property
    def y(self):
        return self._positions[1]
    @y.setter
    def y(self, value):
        self._positions[1] = float(value)

    @property
    def z(self):
        return self._positions[2]
    @z.setter
    def z(self, value):
        self._positions[2] = float(value)

    def _inverse_handedness(self):
        self._positions[0] *= -1.0
        return self

    @classmethod
    def _get_inversed_handedness(cls, value):
        return Vector3(-value.x, value.y, value.z)
