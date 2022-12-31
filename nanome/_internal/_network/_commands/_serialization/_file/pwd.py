from nanome._internal._util._serializers import _StringSerializer, _TypeSerializer
from nanome.util import FileError


class _PWD(_TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "pwd"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        error_code = FileError.safe_cast(context.read_int())
        path = context.read_using_serializer(self.__string)
        return (error_code, path)
