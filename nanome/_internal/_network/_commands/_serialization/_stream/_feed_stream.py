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
        from nanome.api.streams import Stream

        context.write_uint(value[0])
        data_type = value[2]
        if version > 0:
            context.write_byte(data_type)
        if data_type == Stream.DataType.byte:
            context.write_byte_array(value[1])
        elif data_type == Stream.DataType.string:
            context.write_using_serializer(self.__array, value[1])
        else:
            context.write_float_array(value[1])

    def deserialize(self, version, context):
        from nanome.api.streams import Stream

        id = context.read_uint()
        type = Stream.DataType.float
        if version > 0:
            type = Stream.DataType(context.read_byte())

        if type == Stream.DataType.byte:
            data = context.read_byte_array()
        elif type == Stream.DataType.string:
            data = context.read_using_serializer(self.__array)
        else:
            data = context.read_float_array()

        return (id, data, type)
