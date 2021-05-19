from nanome._internal._shapes._shape import _Shape

class Shape(object):
    """
    | Base class of a shape. Used in self.create_shape(shape_type) in plugins.

    :param shape_type: Enumerator representing the shape_type to create
    :type shape_type: :class:`~nanome.util.enums.ShapeType`
    """
    def __init__(self, shape_type):
        _Shape.__init__(self, shape_type)

    @property
    def index(self):
        """
        | Index of the shape
        """
        return self._index

    @property
    def shape_type(self):
        """
        | Type of shape. Currently Sphere, Line, and Label are supported.

        :rtype: :class:`~nanome.util.enums.ShapeType`
        """
        return self.__shape_type

    @property
    def color(self):
        """
        | Get color of the shape

        :rtype: :class:`~nanome.util.Color`
        """
        return self.__color
    @color.setter
    def color(self, value):
        """
        | Set color of the shape

        :param value: Color of the shape
        :type value: :class:`~nanome.util.Color`
        """
        self._color = value

    @property
    def anchors(self):
        """
        | Get anchors of the shape

        :rtype: list of :class:`~nanome.api.shapes.Anchor`
        """
        return self._anchors
    @anchors.setter
    def anchors(self, value):
        """
        | Set anchors of the shape

        :param value: Anchors of the shape
        :type value: list of :class:`~nanome.api.shapes.Anchor`
        """
        self._anchors = value

    def upload(self, done_callback=None):
        self._upload(done_callback)

    def destroy(self):
        """
        | Remove the shape from Nanome App and destroy it.
        """
        self._destroy()
_Shape._create = Shape
