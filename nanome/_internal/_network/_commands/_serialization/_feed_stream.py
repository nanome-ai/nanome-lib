from nanome._internal._util._serializers import _ArraySerializer, _FloatSerializer
from nanome._internal._util._serializers import _TypeSerializer

class _FeedStream(_TypeSerializer):
    def __init__(self):
        self.__array = _ArraySerializer()
        self.__array.set_type(_FloatSerializer())

    def version(self):
        return 0

    def name(self):
        return "StreamFeed"

    def serialize(self, version, value, context):
        context.write_uint(value[0])
        context.write_using_serializer(self.__array, value[1])

    def deserialize(self, version, context):
        raise NotImplementedError