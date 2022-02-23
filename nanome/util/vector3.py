from __future__ import division
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

    def __repr__(self):
        return 'Vector3(x={}, y={}, z={})'.format(*self._positions)

    def __str__(self):
        s = ' '.join([str(self.x), str(self.y), str(self.z)])
        return s

    def __iter__(self):
        return self._positions.__iter__()

    def get_copy(self):
        """
        :return: A copy of this vector.
        :rtype: :class:`~nanome.util.Vector3`
        """
        return Vector3(self.x, self.y, self.z)

    @classmethod
    def cross(cls, v1, v2):
        """
        | Returns the cross product of two vectors.

        :param v1: The first vector
        :type v1: :class:`~nanome.util.Vector3`
        :param v2: The second vector
        :type v2: :class:`~nanome.util.Vector3`
        :return: Cross product of v1 and v2
        :rtype: :class:`~nanome.util.Vector3`
        """
        x = v1.y * v2.z - v1.z * v2.y
        y = v1.z * v2.x - v1.x * v2.z
        z = v1.x * v2.y - v1.y * v2.x
        return Vector3(x, y, z)

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

    @classmethod
    def dot(cls, v1, v2):
        """
        | Returns the dot product of two vectors.

        :param v1: The first vector
        :type v1: :class:`~nanome.util.Vector3`
        :param v2: The second vector
        :type v2: :class:`~nanome.util.Vector3`
        :return: Dot product of v1 and v2
        :rtype: :class:`float`
        """
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    def __pos__(self):
        return self

    def __neg__(self):
        return self * -1

    def __abs__(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar):
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __eq__(self, other):
        if isinstance(other, Vector3):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return NotImplemented

    def __ne__(self, other):
        eq = self == other
        if eq is not NotImplemented:
            return not eq
        return NotImplemented

    def equals(self, other):
        """
        | Returns True if the components of this vector are the same as another's.

        :param other: The other Vector3
        :type other: :class:`~nanome.util.Vector3`
        :return: Whether or not this vector is component-equal to 'other'
        :rtype: :class:`bool`
        """
        return self == other

    def unpack(self):
        """
        :return: a 3-tuple containing this vector's x, y, and z components.
        :rtype: :class:`tuple`
        """
        return self.x, self.y, self.z

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

    def normalize(self):
        """
        | Normalizes this vector and returns itself.

        :return: This vector, now normalized.
        :rtype: :class:`~nanome.util.Vector3`
        """
        length = self.magnitude
        if length > 0:
            self.x /= length
            self.y /= length
            self.z /= length
        return self

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

    @property
    def magnitude(self):
        """
        | The magnitude of this vector

        :type: :class:`float`
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    @property
    def normalized(self):
        """
        | The normalized version of this vector

        :type: :class:`~nanome.util.Vector3`
        """
        if self.magnitude > 0:
            return self / self.magnitude
        return self

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
