from nanome.util import Color
from testing.utilities import run_test
import unittest


def run(counter):
    # Manually call all the things TestCases should do automatically, so that it
    # plays nice with our existing unittests
    testcase = TestColorProperties()
    testcase.setUp()
    run_test(testcase.test_rgb, counter)
    run_test(testcase.test_rgba, counter)


class TestColorProperties(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.color = Color.Black()

    def test_rgb(self):
        rgb = self.color.rgb
        self.assertTrue(isinstance(rgb, tuple))
        self.assertEqual(len(rgb), 3)

    def test_rgba(self):
        rgba = self.color.rgba
        self.assertTrue(isinstance(rgba, tuple))
        self.assertEqual(len(rgba), 4)
