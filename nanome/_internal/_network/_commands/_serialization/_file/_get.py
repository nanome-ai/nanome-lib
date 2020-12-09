from nanome._internal._util._serializers import _StringSerializer
from nanome.util import FileError

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
        error_code = FileError(context.read_int())
        length = context.read_uint()
        file = context.read_bytes(length)
        return (error_code, file)