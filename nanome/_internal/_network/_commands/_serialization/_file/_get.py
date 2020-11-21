from nanome._internal._util._serializers import _StringSerializer, _ArraySerializer, _TupleSerializer, _BytesArraySerializer
from nanome.util import DirectoryErrorCode

from nanome._internal._util._serializers import _TypeSerializer

class _Get(_TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()
        _bytes = _BytesArraySerializer()
        _tuple = _TupleSerializer(self.__string, _bytes)
        self.__array = _ArraySerializer(_tuple)

    def version(self):
        return 0

    def name(self):
        return "get"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)
        context.write_int(len(value[1]))
        context.write_bytes(value[1])

    def deserialize(self, version, context):
        error_code = DirectoryErrorCode(context.read_int())
        files = context.read_using_serializer(self.__array)
        return (error_code, files)