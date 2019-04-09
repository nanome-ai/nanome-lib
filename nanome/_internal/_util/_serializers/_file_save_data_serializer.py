from . import _StringSerializer, _ArraySerializer, _ByteSerializer
from nanome.util import FileErrorCode, FileSaveData, IntEnum

from nanome._internal._util._serializers import _TypeSerializer

class _FileSaveDataSerializer(_TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "FileSaveData"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value.path)
        context.write_int(len(value.data))
        context.write_bytes(value.data)

    def deserialize(self, version, context):
        result = FileSaveData()
        result.path = context.read_using_serializer(self.__string)
        result.error_code = FileErrorCode(context.read_int())
        return result