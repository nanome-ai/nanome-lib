import math


class Vector3(object):
    """
    | A vector that holds 3 values. Used for position and scale.
    """

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
        """
        :return: A copy of this vector.
        :rtype: :class:`~nanome.util.Vector3`
        """
        return Vector3(self._positions[0], self._positions[1], self._positions[2])

    @classmethod
    def distance(cls, v1, v2):
        """
        | Returns the distance between two vectors.

        :param v1: The first vector
        :type v1: :class:`~nanome.util.Vector3`
        :param v2: The second vector
        :type v2: :class:`~nanome.util.Vector3`
        """
        return math.sqrt((v2.x - v1.x) ** 2 + (v2.y - v1.y) ** 2 + (v2.z - v1.z) ** 2)

    def __add__(self, other):
        return Vector3(self._positions[0] + other.x, self._positions[1] + other.y, self._positions[2] + other.z)

    def __sub__(self, other):
        return Vector3(self._positions[0] - other.x, self._positions[1] - other.y, self._positions[2] - other.z)

    def __mul__(self, scalar):
        return Vector3(self._positions[0] * scalar, self._positions[1] * scalar, self._positions[2] * scalar)

    def equals(self, other):
        """
        | Returns True if the components of this vector are the same as another's.

        :param other: The other Vector3
        :type other: :class:`~nanome.util.Vector3`
        :return: Whether or not this vector is component-equal to 'other'
        :rtype: :class:`bool`
        """
        return self.x == other.x and self.y == other.y and self.z == other.z

    def unpack(self):
        """
        :return: a 3-tuple containing this vector's x, y, and z components.
        :rtype: :class:`tuple`
        """
        return self._positions[0], self._positions[1], self._positions[2]

    def set(self, x, y, z):
        """
        :param x: The x component to set this vector to
        :type x: :class:`float`
        :param y: The y component to set this vector to
        :type y: :class:`float`
        :param z: The z component to set this vector to
        :type z: :class:`float`
        """
        self._positions[0] = x
        self._positions[1] = y
        self._positions[2] = z

    @property
    def x(self):
        """
        | The x component of this vector

        :type: :class:`float`
        """
        return self._positions[0]

    @x.setter
    def x(self, value):
        self._positions[0] = float(value)

    @property
    def y(self):
        """
        | The y component of this vector

        :type: :class:`float`
        """
        return self._positions[1]

    @y.setter
    def y(self, value):
        self._positions[1] = float(value)

    @property
    def z(self):
        """
        | The z component of this vector

        :type: :class:`float`
        """
        return self._positions[2]

    @z.setter
    def z(self, value):
        self._positions[2] = float(value)

    def _inverse_handedness(self):
        """
        | Inverts the handedness of this vector and returns itself.

        :return: This vector, now with inverted handedness.
        :rtype: :class:`~nanome.util.Vector3`
        """
        self._positions[0] *= -1.0
        return self

    @classmethod
    def _get_inversed_handedness(cls, value):
        """
        :return: A new Vector3 with inverted handedness from this vector.
        :rtype: :class:`~nanome.util.Vector3`
        """
        return Vector3(-value.x, value.y, value.z)
