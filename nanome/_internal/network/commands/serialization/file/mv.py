from nanome._internal.util.serializers import _StringSerializer, TypeSerializer
from nanome.util import FileError


class _MV(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "mv"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value[0])
        context.write_using_serializer(self.__string, value[1])

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())
