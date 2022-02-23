import unittest

from nanome.util import ComplexUtils, Vector3


class Vector3TestCase(unittest.TestCase):
    def setUp(self):
        super(Vector3TestCase, self).setUp()
        self.v1 = Vector3(0, 1, 2)
        self.v2 = Vector3(2, 4, 8)
        self.v3 = Vector3(2, 0, 0)

    def test_getitem(self):
        self.assertEqual(self.v1[0], 0)
        self.assertEqual(self.v1[1], 1)
        self.assertEqual(self.v1[2], 2)

    def test_setitem(self):
        v = Vector3()
        v[0] = 1
        v[1] = 2
        v[2] = 3
        self.assertEqual(v, Vector3(1, 2, 3))

    def test_repr(self):
        self.assertEqual(repr(self.v1), "Vector3(x=0.0, y=1.0, z=2.0)")

    def test_str(self):
        self.assertEqual(str(self.v1), "0.0 1.0 2.0")

    def test_iter(self):
        i = self.v1.__iter__()
        self.assertEqual(next(i), 0)
        self.assertEqual(next(i), 1)
        self.assertEqual(next(i), 2)

    def test_eq(self):
        self.assertEqual(self.v1, Vector3(0, 1, 2))
        self.assertIs(self.v1 == 0, False)

    def test_neq(self):
        self.assertNotEqual(self.v1, Vector3(0, 1, 3))
        self.assertIs(self.v1 != 0, True)

    def test_pos(self):
        self.assertEqual(+self.v1, self.v1)

    def test_neg(self):
        self.assertEqual(-self.v1, Vector3(-0, -1, -2))

    def test_abs(self):
        self.assertEqual(abs(-self.v1), self.v1)

    def test_add(self):
        self.assertEqual(self.v1 + self.v2, Vector3(2, 5, 10))

    def test_sub(self):
        self.assertEqual(self.v1 - self.v2, Vector3(-2, -3, -6))

    def test_mul(self):
        self.assertEqual(self.v1 * 2, Vector3(0, 2, 4))

    def test_div(self):
        self.assertEqual(self.v2.__truediv__(2), Vector3(1, 2, 4))

    def test_cross(self):
        self.assertEqual(Vector3.cross(self.v1, self.v2), Vector3(0, 4, -2))

    def test_dot(self):
        self.assertEqual(Vector3.dot(self.v1, self.v2), 20)

    def test_distance(self):
        self.assertEqual(Vector3.distance(self.v1, self.v2), 7)

    def test_magnitude(self):
        self.assertEqual(self.v3.magnitude, 2)

    def test_normalized(self):
        self.assertEqual(self.v3.normalized, Vector3(1, 0, 0))

    def test_normalize(self):
        v = self.v3.get_copy()
        v.normalize()
        self.assertEqual(v, Vector3(1, 0, 0))

    def test_unpack(self):
        self.assertEqual(self.v1.unpack(), (0, 1, 2))

    def test_set(self):
        v = Vector3()
        v.set(1, 2, 3)
        self.assertEqual(v, Vector3(1, 2, 3))
