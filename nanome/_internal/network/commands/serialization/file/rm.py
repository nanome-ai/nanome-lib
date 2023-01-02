from nanome._internal.util.serializers import _StringSerializer, TypeSerializer
from nanome.util import FileError


class _RM(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "rm"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())
