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
        def set_callback(indices, results):
            index = indices[0]
            result = results[0]
            if self._index != -1 and index != self._index:
                Logs.error("SetShapeCallback received for the wrong shape")
            self._index = index
            if done_callback is not None:
                done_callback(result)

        id = nanome._internal._network.PluginNetwork._instance._send(nanome._internal._network._commands._callbacks._Messages.set_shape, [self], True)
        result = nanome.PluginInstance._save_callback(id, set_callback if done_callback else None)
        if done_callback is None and nanome.PluginInstance._instance.is_async:
            result.real_set_result = result.set_result
            result.set_result = lambda args: set_callback(*args)
            done_callback = lambda *args: result.real_set_result(args)
        return result

    @classmethod
    def _upload_multiple(cls, shapes, done_callback=None):
        def set_callback(indices, results):
            error = False
            for index, shape in zip(indices, shapes):
                if shape._index != -1 and index != shape._index:
                    error = True
                shape._index = index
            if error:
                Logs.error("SetShapeCallback received for the wrong shape")
            if done_callback is not None:
                done_callback(results)

        id = nanome._internal._network.PluginNetwork._instance._send(nanome._internal._network._commands._callbacks._Messages.set_shape, shapes, True)
        result = nanome.PluginInstance._save_callback(id, set_callback if done_callback else None)
        if done_callback is None and nanome.PluginInstance._instance.is_async:
            result.real_set_result = result.set_result
            result.set_result = lambda args: set_callback(*args)
            done_callback = lambda *args: result.real_set_result(args)
        return result

    def _destroy(self, done_callback=None):
        def set_callback(indices):
            if done_callback is not None:
                done_callback(indices)

        id = nanome._internal._network.PluginNetwork._instance._send(nanome._internal._network._commands._callbacks._Messages.delete_shape, [self._index], True)
        result = nanome.PluginInstance._save_callback(id, set_callback if done_callback else None)
        if done_callback is None and nanome.PluginInstance._instance.is_async:
            result.real_set_result = result.set_result
            result.set_result = lambda args: set_callback(args)
            def done_callback(args): return result.real_set_result(args)
        return result

    @classmethod
    def _destroy_multiple(cls, shapes, done_callback=None):
        def set_callback(indices):
            if done_callback is not None:
                done_callback(indices)

        indices = [x._index for x in shapes]
        id = nanome._internal._network.PluginNetwork._instance._send(nanome._internal._network._commands._callbacks._Messages.delete_shape, indices, True)
        result = nanome.PluginInstance._save_callback(id, set_callback if done_callback else None)
        if done_callback is None and nanome.PluginInstance._instance.is_async:
            result.real_set_result = result.set_result
            result.set_result = lambda args: set_callback(args)
            def done_callback(args): return result.real_set_result(args)
        return result
