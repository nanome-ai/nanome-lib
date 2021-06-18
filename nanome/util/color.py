class Color(object):
    """
    | Represents a 32-bit color with red, green, blue and alpha channels (8 bits each).

    :param r: Red component
    :type r: :class:`int`
    :param g: Green component
    :type g: :class:`int`
    :param b: Blue component
    :type b: :class:`int`
    :param a: Alpha component
    :type a: :class:`int`
    :param whole_num: Optional way to input color. The int or hex form of the color. e.g. 0x8000FFFF
    :type whole_num: :class:`int` or hex
    """

    def __init__(self, r=0, g=0, b=0, a=255, whole_num=None):
        if whole_num is not None:
            self.set_color_int(whole_num)
        else:
            self.set_color_rgb(r, g, b, a)

    def set_color_int(self, num):
        """
        | Assigns the color an integer value representing
        | the red component bitshifted 24 bits, bitwise ORed with
        | the green component bitshifted 16 bits, bitwise ORed with
        | the blue component bitshifted 8 bits, ORed with
        | the alpha component, or more simply:
        | r << 24 | g << 16 | b << 8 | a
        | OR
        | 0xRRGGBBAA

        :param num: Number to set the color to
        :type num: :class:`int`
        """
        self._color = num

    def set_color_rgb(self, r=0, g=0, b=0, a=255):
        """
        | Assign a value by individual color components.

        :param r: Red component
        :type r: :class:`int` (0-255)
        :param g: Green component
        :type g: :class:`int` (0-255)
        :param b: Blue component
        :type b: :class:`int` (0-255)
        :param a: Alpha component
        :type a: :class:`int` (0-255)
        """
        r = max(0, min(int(r), 255))
        g = max(0, min(int(g), 255))
        b = max(0, min(int(b), 255))
        a = max(0, min(int(a), 255))
        self._color = r << 24 | g << 16 | b << 8 | a

    @classmethod
    def from_int(cls, value):
        """
        | Set color from int after initializing.

        :param value: Int value of the color
        :type value: :class:`int`
        """
        if (value < 0):  # convert to uint
            value += 4294967295  # max int
        value = int(value)
        color = Color(whole_num=value)
        return color

    # presets
    @classmethod
    def Black(cls):
        return Color(whole_num=255)

    @classmethod
    def Red(cls):
        return Color(whole_num=0xFF0000FF)

    @classmethod
    def Green(cls):
        return Color(whole_num=0x00FF00FF)

    @classmethod
    def Blue(cls):
        return Color(whole_num=0x0000FFFF)

    @classmethod
    def White(cls):
        return Color(whole_num=0xFFFFFFFF)

    @classmethod
    def Clear(cls):
        return Color(whole_num=0)

    @classmethod
    def Grey(cls):
        return Color(whole_num=0x7F7F7FFF)

    @classmethod
    def Gray(cls):
        return Color(whole_num=0x7F7F7FFF)

    @classmethod
    def Yellow(cls):
        return Color(whole_num=0xFFEB04FF)

    # operators

    # <color,color>

    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b, self.a + other.a)

    def __sub__(self, other):
        return Color(self.r - other.r, self.g - other.g, self.b - other.b, self.a - other.a)

    # <color, float>
    def __mul__(self, number):
        return Color(self.r * number, self.g * number, self.b * number, self.a * number)

    def __truediv__(self, number):
        return Color(self.r / number, self.g / number, self.b / number, self.a / number)

    # properties
    @property
    def r(self):
        """
        | The red component of the color.

        :type: :class:`int`
        """
        return self._color >> 24 & 0x000000FF

    @r.setter
    def r(self, value):
        value = min(max(int(value), 0), 255)
        self._color = 0x00FFFFFF & self._color | (value << 24)

    @property
    def g(self):
        """
        | The green component of the color.

        :type: :class:`int`
        """
        return self._color >> 16 & 0x000000FF

    @g.setter
    def g(self, value):
        value = min(max(int(value), 0), 255)
        self._color = 0xFF00FFFF & self._color | (value << 16)

    @property
    def b(self):
        """
        | The blue component of the color.

        :type: :class:`int`
        """
        return self._color >> 8 & 0x000000FF

    @b.setter
    def b(self, value):
        value = min(max(int(value), 0), 255)
        self._color = 0xFFFF00FF & self._color | (value << 8)

    @property
    def a(self):
        """
        | The alpha component of the color.

        :type: :class:`int`
        """
        return self._color & 0x000000FF

    @a.setter
    def a(self, value):
        value = min(max(int(value), 0), 255)
        self._color = 0xFFFFFF00 & self._color | value

    # functions
    def copy(self):
        """
        | Create a new color from this one.

        :rtype: :class:`~nanome.util.Color`
        """
        return Color(whole_num=self._color)

    def to_string_hex(self):
        """
        | Returns a hex string representing the color.

        :rtype: class:`str`
        """
        return hex(self._color)

    @property
    def rgb(self):
        return (self.r, self.g, self.b)

    @property
    def rgba(self):
        return (self.r, self.g, self.b, self.a)
