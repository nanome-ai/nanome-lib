from . import _StringSerializer, _ArraySerializer, _ByteSerializer
from nanome.util import FileErrorCode, FileData, IntEnum

from nanome._internal.util.serializers import TypeSerializer


class _FileDataSerializer(TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "FileData"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        result = FileData()
        count = context.read_int()
        result.data = context.read_bytes(count)
        result.error_code = FileErrorCode(context.read_int())
        return result
