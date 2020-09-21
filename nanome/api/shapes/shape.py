import nanome
from nanome._internal._network._commands._callbacks import _Messages
from nanome.util import Vector3, Color, Logs, Quaternion
from nanome.util.enums import ShapeAnchorType

class Shape(object):
    def __init__(self, network, shape_type):
        self.__network = network

        self.__index = -1
        self.__target = 0
        self.__shape_type = shape_type
        self.__anchor = ShapeAnchorType.Workspace
        self.__position = Vector3()
        self.__rotation = Quaternion()
        self.__color = Color()

    @property
    def index(self):
        return self.__index

    @property
    def shape_type(self):
        return self.__shape_type

    @property
    def target(self):
        return self.__target
    @target.setter
    def target(self, value):
        self.__target = value

    @property
    def anchor(self):
        return self.__anchor
    @anchor.setter
    def anchor(self, value):
        self.__anchor = value

    @property
    def position(self):
        return self.__position
    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def rotation(self):
        return self.__rotation
    @rotation.setter
    def rotation(self, value):
        self.__rotation = value

    @property
    def color(self):
        return self.__color
    @color.setter
    def color(self, value):
        self.__color = value

    def upload(self, done_callback=None):
        def set_callback(index, result):
            if self.__index != -1 and index != self.__index:
                Logs.error("SetShapeCallback received for the wrong shape")
            self.__index = index
            if done_callback != None:
                done_callback(result)

        id = self.__network._send(_Messages.set_shape, self, True)
        nanome.PluginInstance._save_callback(id, set_callback)

    def destroy(self):
        self.__network._send(_Messages.delete_shape, self.__index, False)