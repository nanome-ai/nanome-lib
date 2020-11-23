from nanome._internal._util._serializers import _StringSerializer, _ArraySerializer, _TupleSerializer, _BytesArraySerializer
from nanome.util import DirectoryErrorCode

from nanome._internal._util._serializers import _TypeSerializer

class _Get(_TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "get"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        error_code = DirectoryErrorCode(context.read_int())
        name = context.read_using_serializer(self.__string)
        length = context.read_uint()
        file = context.read_bytes(length)
        return (error_code, name, file)