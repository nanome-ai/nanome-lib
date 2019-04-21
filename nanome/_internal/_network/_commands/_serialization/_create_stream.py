from nanome._internal._util._serializers import _ArraySerializer, _LongSerializer
from nanome._internal._util._serializers import _TypeSerializer

class _CreateStream(_TypeSerializer):
    def __init__(self):
        self.__array = _ArraySerializer()
        self.__array.set_type(_LongSerializer())

    def version(self):
        return 0

    def name(self):
        return "StreamCreation"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__array, value)

    def deserialize(self, version, context):
        raise NotImplementedError