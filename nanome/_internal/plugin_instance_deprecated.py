import nanome
from . import _PluginInstance
from nanome._internal._network._commands._callbacks import _Messages
from nanome.util import DirectoryRequestOptions
from nanome.util.enums import ShapeType
from nanome._internal import _shapes


@nanome.util.Logs.deprecated("files.ls")
def _request_directory(self, path, callback=None, pattern="*"):
    """
    | Requests the content of a directory on the machine running Nanome

    :param path: Path to request. E.g. "." means Nanome's running directory
    :type path: str
    :param pattern: Pattern to match. E.g. "*.txt" will match all .txt files. Default value is "*" (match everything)
    :type pattern: str
    """
    options = DirectoryRequestOptions()
    options._directory_name = path
    options._pattern = pattern
    id = self._network._send(_Messages.directory_request, options, callback != None)
    self._save_callback(id, callback)


_PluginInstance.request_directory = _request_directory


@nanome.util.Logs.deprecated("files.get")
def _request_files(self, file_list, callback=None):
    """
    | Reads files on the machine running Nanome, and returns them

    :param file_list: List of file name (with path) to read. E.g. ["a.sdf", "../b.sdf"] will read a.sdf in running directory, b.sdf in parent directory, and return them
    :type file_list: list of :class:`str`
    """
    id = self._network._send(_Messages.file_request, file_list, callback != None)
    self._save_callback(id, callback)


_PluginInstance.request_files = _request_files


@nanome.util.Logs.deprecated()
def _create_shape(self, shape_type):
    if shape_type == ShapeType.Sphere:
        return _shapes._Sphere._create()
    if shape_type == ShapeType.Line:
        return _shapes._Line._create()

    raise ValueError('Parameter shape_type must be a value of nanome.util.enums.ShapeType')


_PluginInstance.create_shape = _create_shape
