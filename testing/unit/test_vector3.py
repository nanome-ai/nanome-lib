from __future__ import division
import unittest

from nanome.util import Vector3


class Vector3TestCase(unittest.TestCase):
    def test_getitem(self):
        v = Vector3(0, 1, 2)
        self.assertEqual(v[0], 0)
        self.assertEqual(v[1], 1)
        self.assertEqual(v[2], 2)

    def test_setitem(self):
        v = Vector3()
        v[0] = 1
        v[1] = 2
        v[2] = 3
        expected = Vector3(1, 2, 3)
        self.assertEqual(v, expected)

    def test_repr(self):
        v = Vector3(0, 1, 2)
        expected = "Vector3(x=0.0, y=1.0, z=2.0)"
        self.assertEqual(repr(v), expected)

    def test_str(self):
        v = Vector3(0, 1, 2)
        expected = "0.0 1.0 2.0"
        self.assertEqual(str(v), expected)

    def test_iter(self):
        v = Vector3(0, 1, 2)
        i = v.__iter__()
        self.assertEqual(next(i), 0)
        self.assertEqual(next(i), 1)
        self.assertEqual(next(i), 2)

    def test_eq(self):
        v = Vector3(0, 1, 2)
        expected = Vector3(0, 1, 2)
        self.assertEqual(v, expected)
        self.assertIs(v == 0, False)

    def test_neq(self):
        v = Vector3(0, 1, 2)
        expected = Vector3(0, 1, 3)
        self.assertNotEqual(v, expected)
        self.assertIs(v != 0, True)

    def test_pos(self):
        v = Vector3(0, 1, 2)
        self.assertEqual(+v, v)

    def test_neg(self):
        v = Vector3(0, 1, 2)
        expected = Vector3(-0, -1, -2)
        self.assertEqual(-v, expected)

    def test_abs(self):
        v = Vector3(0, 1, 2)
        self.assertEqual(abs(-v), v)

    def test_add(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(2, 4, 8)
        expected = Vector3(2, 5, 10)
        self.assertEqual(v1 + v2, expected)

    def test_sub(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(2, 4, 8)
        expected = Vector3(-2, -3, -6)
        self.assertEqual(v1 - v2, expected)

    def test_mul(self):
        v = Vector3(0, 1, 2)
        expected = Vector3(0, 2, 4)
        self.assertEqual(v * 2, expected)

    def test_div(self):
        v = Vector3(2, 4, 8)
        expected = Vector3(1, 2, 4)
        self.assertEqual(v / 2, expected)

    def test_cross(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(2, 4, 8)
        expected = Vector3(0, 4, -2)
        self.assertEqual(Vector3.cross(v1, v2), expected)

    def test_dot(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(2, 4, 8)
        self.assertEqual(Vector3.dot(v1, v2), 20)

    def test_distance(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(2, 4, 8)
        self.assertEqual(Vector3.distance(v1, v2), 7)

    def test_magnitude(self):
        v = Vector3(2, 0, 0)
        self.assertEqual(v.magnitude, 2)

    def test_normalized(self):
        v = Vector3(2, 0, 0)
        expected = Vector3(1, 0, 0)
        self.assertEqual(v.normalized, expected)

    def test_normalize(self):
        v = Vector3(2, 0, 0)
        v.normalize()
        expected = Vector3(1, 0, 0)
        self.assertEqual(v, expected)

    def test_unpack(self):
        v = Vector3(0, 1, 2)
        self.assertEqual(v.unpack(), (0, 1, 2))

    def test_set(self):
        v = Vector3()
        v.set(1, 2, 3)
        expected = Vector3(1, 2, 3)
        self.assertEqual(v, expected)
