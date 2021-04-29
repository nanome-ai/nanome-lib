import nanome
from nanome.util import Color, Logs

class _Shape(object):
    def __init__(self, shape_type):
        self._index = -1
        self._shape_type = shape_type
        self._anchors = []
        self._color = Color.Grey()

    @classmethod
    def _create(cls, shape_type):
        return cls(shape_type)

    def _upload(self, done_callback=None):
        def set_callback(index, result):
            if self._index != -1 and index != self._index:
                Logs.error("SetShapeCallback received for the wrong shape")
            self._index = index
            if done_callback != None:
                done_callback(result)

        id = nanome._internal._network._ProcessNetwork._instance._send(nanome._internal._network._commands._callbacks._Messages.set_shape, self, True)
        nanome.PluginInstance._save_callback(id, set_callback)

    def _destroy(self):
        nanome._internal._network._ProcessNetwork._instance._send(nanome._internal._network._commands._callbacks._Messages.delete_shape, self._index, False)