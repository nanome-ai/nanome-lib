import nanome
from nanome._internal._shapes._shape import _Shape
from nanome.util import Logs

try:
    import asyncio
except ImportError:
    asyncio = False


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
        | Upload multiple shapes to the Nanome App
        """
        try:
            return _Shape._upload_multiple(shapes, done_callback)
        except TypeError:
            # If upload multiple fails, upload each one at a time.
            # Done as a fallback for older versions of Nanome that don't support
            # upload_multiple yet
            Logs.warning('upload_multiple() failed, attempting to upload one at a time.')

            # Make sure fallback works for async calls
            future = None
            if done_callback is None and nanome.PluginInstance._instance.is_async:
                loop = asyncio.get_event_loop()
                future = loop.create_future()
                done_callback = lambda *args: future.set_result(args)

            results = []

            def upload_callback(result):
                results.append(result)
                if len(results) == len(shapes):
                    done_callback(results)

            for shape in shapes:
                shape.upload(upload_callback if done_callback else None)

            return future

    def destroy(self):
        """
        | Remove the shape from the Nanome App and destroy it.
        """
        self._destroy()

    @classmethod
    def destroy_multiple(cls, shapes, done_callback=None):
        """
        | Remove multiple shapes from the Nanome App and destroy them.
        """
        try:
            _Shape._destroy_multiple(shapes)
        except TypeError:
            # If destroy multiple fails, upload each one at a time.
            # Done as a fallback for older versions of Nanome that don't support
            # destroy_multiple yet
            Logs.warning('destroy_multiple() failed, attempting to destroy one at a time.')
            for shape in shapes:
                shape.destroy()


_Shape._create = Shape
