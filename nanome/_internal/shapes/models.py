# from nanome._internal.network import nanome._internal.network.PluginNetwork
import logging
from nanome._internal.enums import Messages
from nanome._internal.network import PluginNetwork

logger = logging.getLogger(__name__)


class _Shape(object):
    def __init__(self, shape_type):
        from nanome.util import Color
        self._index = -1
        self._shape_type = shape_type
        self._anchors = []
        self._color = Color.Grey()

    @classmethod
    def _create(cls, shape_type):
        return cls(shape_type)

    def _upload(self, done_callback=None):
        import nanome

        def set_callback(indices, results):
            index = indices[0]
            result = results[0]
            if self._index != -1 and index != self._index:
                logger.error("SetShapeCallback received for the wrong shape")
            self._index = index
            if done_callback is not None:
                done_callback(result)

        id = PluginNetwork._instance.send(Messages.set_shape, [self], True)
        result = nanome.PluginInstance._save_callback(
            id, set_callback if done_callback else None)
        if done_callback is None and nanome.PluginInstance._instance.is_async:
            result.real_set_result = result.set_result
            result.set_result = lambda args: set_callback(*args)
            done_callback = lambda *args: result.real_set_result(args)
        return result

    @classmethod
    def _upload_multiple(cls, shapes, done_callback=None):
        import nanome

        def set_callback(indices, results):
            error = False
            for index, shape in zip(indices, shapes):
                if shape._index != -1 and index != shape._index:
                    error = True
                shape._index = index
            if error:
                logger.error("SetShapeCallback received for the wrong shape")
            if done_callback is not None:
                done_callback(results)

        id = PluginNetwork._instance.send(Messages.set_shape, shapes, True)
        result = nanome.PluginInstance._save_callback(
            id, set_callback if done_callback else None)
        if done_callback is None and nanome.PluginInstance._instance.is_async:
            result.real_set_result = result.set_result
            result.set_result = lambda args: set_callback(*args)
            done_callback = lambda *args: result.real_set_result(args)
        return result

    def _destroy(self, done_callback=None):
        import nanome

        def set_callback(indices):
            if done_callback is not None:
                done_callback(indices)
        id = PluginNetwork._instance.send(
            Messages.delete_shape, [self._index], True)
        result = nanome.PluginInstance._save_callback(
            id, set_callback if done_callback else None)
        if done_callback is None and nanome.PluginInstance._instance.is_async:
            result.real_set_result = result.set_result
            result.set_result = lambda args: set_callback(args)
            def done_callback(args): return result.real_set_result(args)
        return result

    @classmethod
    def _destroy_multiple(cls, shapes, done_callback=None):
        import nanome

        def set_callback(indices):
            if done_callback is not None:
                done_callback(indices)

        indices = [x._index for x in shapes]
        id = PluginNetwork._instance.send(Messages.delete_shape, indices, True)
        result = nanome.PluginInstance._save_callback(
            id, set_callback if done_callback else None)
        if done_callback is None and nanome.PluginInstance._instance.is_async:
            result.real_set_result = result.set_result
            result.set_result = lambda args: set_callback(args)
            def done_callback(args): return result.real_set_result(args)
        return result


class _Anchor(object):
    def __init__(self):
        from nanome.util import Vector3
        from nanome.util.enums import ShapeAnchorType
        self._target = 0
        self._local_offset = Vector3()
        self._global_offset = Vector3()
        self._viewer_offset = Vector3()
        self._anchor_type = ShapeAnchorType.Workspace

    @classmethod
    def _create(cls):
        return cls()


class _Label(_Shape):
    def __init__(self):
        from nanome.util.enums import ShapeType
        _Shape.__init__(self, ShapeType.Label)
        self._anchors = [_Anchor._create()]
        self._text = ""
        self._font_size = .5

    @classmethod
    def _create(cls):
        return cls()


class _Line(_Shape):
    def __init__(self):
        from nanome.util.enums import ShapeType
        _Shape.__init__(self, ShapeType.Line)
        self._anchors = [_Anchor._create(), _Anchor._create()]
        self._thickness = 0.1
        self._dash_length = 0.4
        self._dash_distance = 0.1

    @classmethod
    def _create(cls):
        return cls()


class _Mesh(_Shape):
    def __init__(self):
        from nanome.util.enums import ShapeType
        _Shape.__init__(self, ShapeType.Mesh)
        self._anchors = [_Anchor._create()]
        self._vertices = []
        self._normals = []
        self._colors = []
        self._triangles = []
        self._uv = []
        self._texture_path = ""
        self._unlit = False

    @classmethod
    def _create(cls):
        return cls()


class _Sphere(_Shape):
    def __init__(self):
        from nanome.util.enums import ShapeType
        _Shape.__init__(self, ShapeType.Sphere)
        self._anchors = [_Anchor._create()]
        self._radius = 1.0

    @classmethod
    def _create(cls):
        return cls()
