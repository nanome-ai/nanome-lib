import math
#placeholder quaternion

class Quaternion(object):
    def __init__(self, x=0, y=0, z=0, w=1):
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

    def get_copy(self):
        return Quaternion(self.x,self.y,self.z,self.w)

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

    def _inverse_handedness(self):
        self._y *= -1.0
        self._z *= -1.0
        return self

    def get_conjugate(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    @classmethod
    def _get_inversed_handedness(cls, value):
        return Quaternion(value.x, -value.y, -value.z, value.w)

    def __mul__(self, other):
        q =self
        if isinstance(other, Quaternion):
            r = other
            w = r.w * q.w - r.x * q.x - r.y * q.y - r.z * q.z
            x = r.w * q.x + r.x * q.w - r.y * q.z + r.z * q.y
            y = r.w * q.y + r.x * q.z + r.y * q.w - r.z * q.x
            z = r.w * q.z - r.x * q.y + r.y * q.x + r.z * q.w
            return Quaternion(x,y,z,w)
        elif (isinstance(other, float) or isinstance(other, int)):
            n = other
            return Quaternion(q.x * n, q.y * n, q.z * n, q.w * n)
        else:
            raise NotImplementedError

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    EPS = 1*(10**-6)
    def equals(self, other):
        return abs(self.dot(other)) > 1-Quaternion.EPS

    def rotate_vector(self, point):
        r = Quaternion(point.x, point.y, point.z, 0)
        q_conj = self.get_conjugate()
        result = ((self * r) * q_conj)
        point = point.get_copy()
        point.x = result.x
        point.y = result.y
        point.z = result.z
        return point

    #algorithm credit https://d3cw3dd2w32x2b.cloudfront.net/wp-content/uploads/2015/01/matrix-to-quat.pdf
    @classmethod
    def from_matrix(cls, matrix):
        m = matrix
        if (m[2][2] < 0):
            if (m[0][0] > m[1][1]):
                t = 1 + m[0][0] - m[1][1] - m[2][2]
                q = cls( t, m[1][0]+m[0][1], m[0][2]+m[2][0], m[2][1]-m[1][2] )
            else:
                t = 1 - m[0][0] + m[1][1] - m[2][2]
                q = cls( m[1][0]+m[0][1], t, m[2][1]+m[1][2], m[0][2]-m[2][0] )
        else:
            if (m[0][0] < -m[1][1]):
                t = 1 - m[0][0] - m[1][1] + m[2][2]
                q = cls( m[0][2]+m[2][0], m[2][1]+m[1][2], t, m[1][0]-m[0][1] )
            else:
                t = 1 + m[0][0] + m[1][1] + m[2][2]
                q = cls( m[2][1]-m[1][2], m[0][2]-m[2][0], m[1][0]-m[0][1], t )
        q *= 0.5 / math.sqrt(t)
        return q