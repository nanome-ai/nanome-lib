from nanome._internal._util._serializers import _TypeSerializer, _StringSerializer, _ArraySerializer
from nanome._internal._network._commands._serialization._file._file_meta import _FileMeta
from nanome.util import FileError


class _LS(_TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()
        self.__array = _ArraySerializer()
        self.__array.set_type(_FileMeta())

    def version(self):
        return 0

    def name(self):
        return "ls"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        error_code = FileError.safe_cast(context.read_int())
        filemetas = context.read_using_serializer(self.__array)
        return error_code, filemetas
