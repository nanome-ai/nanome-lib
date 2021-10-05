from nanome.util import Color
import unittest


class TestColorProperties(unittest.TestCase):
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
