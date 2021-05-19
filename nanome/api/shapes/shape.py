from nanome._internal._shapes._shape import _Shape

class Shape(object):
    """
    | Base class of a shape. Used in self.create_shape(shape_type) in plugins.

    :param network: Network to send shape to. Usually from plugin_instance's network
    :param shape_type: Enumerator representing the shape_type to create
    :type network: nanome._internal._network
    :type shape_type: :class:`~nanome.util.enums.ShapeType`
    """
    def __init__(self, shape_type):
        _Shape.__init__(self, shape_type)

    @property
    def index(self):
        """
        | Index of the shape
        """
        return self.__index

    @property
    def shape_type(self):
        """
        | Type of shape. Currently only supports spheres.
        """
        return self.__shape_type

    @property
    def target(self):
        """
        | Target object to center the shape on.

        :param value: Object to center the shape on
        :type value: Object
        """
        return self.__target
    @target.setter
    def target(self, value):
        self.__target = value

    @property
    def anchor(self):
        """
        | Type of object we are anchoring the shape on

        :param value: Type of target object
        :type value: :class:`~nanome.util.enums.ShapeAnchorType`
        """
        return self.__anchor
    @anchor.setter
    def anchor(self, value):
        self.__anchor = value

    @property
    def position(self):
        """
        | Position of the shape

        :param value: Position of the shape
        :type value: :class:`~nanome.util.Vector3`
        """
        return self.__position
    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def rotation(self):
        """
        | Rotation of the shape

        :param value: Rotation of the shape
        :type value: :class:`~nanome.util.Quaternion`
        """
        return self.__rotation
    @rotation.setter
    def rotation(self, value):
        self.__rotation = value

    @property
    def color(self):
        """
        | Color of the shape

        :param value: Color of the shape
        :type value: :class:`~nanome.util.Color`
        """
        return self.__color
    @color.setter
    def color(self, value):
        self._color = value

    def upload(self, done_callback=None):
        """
        | Upload the shape to Nanome App.
        """
        def set_callback(index, result):
            if self.__index != -1 and index != self.__index:
                Logs.error("SetShapeCallback received for the wrong shape")
            self.__index = index
            if done_callback != None:
                done_callback(result)

    def upload(self, done_callback=None):
        self._upload(done_callback)

    def destroy(self):
        """
        | Remove the shape from Nanome App and destroy it.
        """
        self.__network._send(_Messages.delete_shape, self.__index, False)
