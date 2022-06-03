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

    def test_hex(self):
        color = Color.Red()
        hex = color.hex
        assert isinstance(hex, str)
        assert hex == '#ff0000ff'

    def test_from_hex_rgb(self):
        color = Color.from_hex('#f00')
        assert isinstance(color, Color)
        assert color.rgba == (255, 0, 0, 255)

    def test_from_hex_rgba(self):
        color = Color.from_hex('#f001')
        assert isinstance(color, Color)
        assert color.rgba == (255, 0, 0, 17)

    def test_from_hex_rrggbb(self):
        color = Color.from_hex('#ff0000')
        assert isinstance(color, Color)
        assert color.rgba == (255, 0, 0, 255)

    def test_from_hex_rrggbbaa(self):
        color = Color.from_hex('#ff0000ff')
        assert isinstance(color, Color)
        assert color.rgba == (255, 0, 0, 255)

    def test_from_hex_invalid_hex(self):
        with self.assertRaises(ValueError):
            Color.from_hex('#f00g')

    def test_from_hex_invalid_len(self):
        with self.assertRaises(ValueError):
            Color.from_hex('#ff')
