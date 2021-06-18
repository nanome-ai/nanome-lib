from nanome.util import Color
from testing.utilities import run_test


def run(counter):
    testcase = TestColorProperties()
    run_test(testcase.test_rgb, counter)
    run_test(testcase.test_rgba, counter)


class TestColorProperties:

    def test_rgb(self):
        color = Color.Black()
        rgb = color.rgb
        assert isinstance(rgb, tuple)
        assert len(rgb) == 3

    def test_rgba(self):
        color = Color.Black()
        rgba = color.rgba
        assert isinstance(rgba, tuple)
        assert len(rgba) == 4
