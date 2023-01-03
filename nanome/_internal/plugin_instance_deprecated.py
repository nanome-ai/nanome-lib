from . import _PluginInstance
from nanome._internal.util.decorators import deprecated
from nanome._internal.network.enums import Messages
from nanome._internal import shapes as internal_shapes


@deprecated("files.ls")
def _request_directory(self, path, callback=None, pattern="*"):
    """
    | Requests the content of a directory on the machine running Nanome

    :param path: Path to request. E.g. "." means Nanome's running directory
    :type path: str
    :param pattern: Pattern to match. E.g. "*.txt" will match all .txt files. Default value is "*" (match everything)
    :type pattern: str
    """
    from nanome.util import DirectoryRequestOptions
    options = DirectoryRequestOptions()
    options._directory_name = path
    options._pattern = pattern
    id = self._network.send(Messages.directory_request, options, callback != None)
    self._save_callback(id, callback)


_PluginInstance.request_directory = _request_directory


@deprecated("files.get")
def _request_files(self, file_list, callback=None):
    """
    | Reads files on the machine running Nanome, and returns them

    :param file_list: List of file name (with path) to read. E.g. ["a.sdf", "../b.sdf"] will read a.sdf in running directory, b.sdf in parent directory, and return them
    :type file_list: list of :class:`str`
    """
    id = self._network.send(Messages.file_request, file_list, callback != None)
    self._save_callback(id, callback)


_PluginInstance.request_files = _request_files


@deprecated()
def _create_shape(self, shape_type):
    from nanome.util.enums import ShapeType
    if shape_type == ShapeType.Sphere:
        return internal_shapes._Sphere._create()
    if shape_type == ShapeType.Line:
        return internal_shapes._Line._create()

    raise ValueError('Parameter shape_type must be a value of nanome.util.enums.ShapeType')


_PluginInstance.create_shape = _create_shape
