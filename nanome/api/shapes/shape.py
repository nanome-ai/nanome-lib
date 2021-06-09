from nanome._internal._shapes._shape import _Shape


class Shape(_Shape):
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
        return self._shape_type

    @property
    def color(self):
        """
        | Color of the shape

        :param value: Color of the shape
        :type value: :class:`~nanome.util.Color`
        """
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def anchors(self):
        """
        | Anchors of the shape

        :param value: Anchors of the shape
        :type value: list of :class:`~nanome.shapes.Anchor`
        """
        return self._anchors

    @anchors.setter
    def anchors(self, value):
        self._anchors = value

    def upload(self, done_callback=None):
        """
        | Upload the shape to the Nanome App
        """
        return self._upload(done_callback)

    @classmethod
    def upload_multiple(cls, shapes, done_callback=None):
        """
        | Upload the shape to the Nanome App
        """
        return _Shape._upload_multiple(shapes, done_callback)

    def destroy(self):
        """
        | Remove the shape from the Nanome App and destroy it.
        """
        self._destroy()


_Shape._create = Shape
