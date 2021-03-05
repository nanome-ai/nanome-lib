import nanome
from nanome._internal._network._commands._callbacks import _Messages
from nanome.util import Color, Logs

class _Shape(object):
    def __init__(self, network, shape_type):
        self.__network = network
        self._index = -1
        self._shape_type = shape_type
        self._anchors = []
        self._color = Color()

    def _upload(self, done_callback=None):
        def set_callback(index, result):
            if self._index != -1 and index != self._index:
                Logs.error("SetShapeCallback received for the wrong shape")
            self._index = index
            if done_callback != None:
                done_callback(result)

        id = self.__network._send(_Messages.set_shape, self, True)
        nanome.PluginInstance._save_callback(id, set_callback)

    def _destroy(self):
        self.__network._send(_Messages.delete_shape, self._index, False)