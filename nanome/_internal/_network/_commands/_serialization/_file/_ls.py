from nanome._internal._util._serializers import _StringSerializer, _ArraySerializer
from nanome.util import DirectoryErrorCode
from nanome._internal._network._commands._serialization._file._file_meta import _FileMeta

from nanome._internal._util._serializers import _TypeSerializer

class _LS(_TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()
        _file_meta = _FileMeta()
        self.__array = _ArraySerializer(_file_meta)

    def version(self):
        return 0

    def name(self):
        return "ls"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        error_code = DirectoryErrorCode.safe_cast(context.read_int())
        filemetas = context.read_using_serializer(self.__array)
        return error_code, filemetas