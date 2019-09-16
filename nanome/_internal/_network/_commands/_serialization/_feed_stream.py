import nanome
from nanome._internal._util._serializers import _TypeSerializer, _ArraySerializer, _StringSerializer

class _FeedStream(_TypeSerializer):
    def __init__(self):
        self.__array = _ArraySerializer()
        self.__array.set_type(_StringSerializer())

    def version(self):
        return 2

    def name(self):
        return "StreamFeed"

    def serialize(self, version, value, context):
        context.write_uint(value[0])
        data_type = value[2]
        if version > 0:
            context.write_byte(data_type)
        if data_type == nanome.api.streams.Stream.DataType.byte:
            context.write_byte_array(value[1])
        elif data_type == nanome.api.streams.Stream.DataType.string:
            context.write_using_serializer(self.__array, value[1])
        else:
            context.write_float_array(value[1])

    def deserialize(self, version, context):
        id = context.read_uint()
        type = nanome.api.streams.Stream.DataType.float
        if version > 0:
            type = nanome.api.streams.Stream.DataType(context.read_byte())

        if type == nanome.api.streams.Stream.DataType.byte:
            data = context.read_byte_array()
        elif type == nanome.api.streams.Stream.DataType.string:
            data = context.read_using_serializer(self._array)
        else:
            data = context.read_float_array()

        return (id, data, type)
