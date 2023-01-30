from nanome._internal import serializer_fields
from nanome.api.streams import Stream
from nanome.util.enums import StreamDataType, StreamDirection, StreamType


class CreateStream(serializer_fields.TypeSerializer):
    def version(self):
        return 2

    def name(self):
        return "StreamCreation"

    def serialize(self, version, value, context):
        stream_type = value[0]
        if version > 0:
            context.write_byte(stream_type)
        if version >= 2:
            context.write_byte(value[2])

        if stream_type == StreamType.shape_position or stream_type == StreamType.shape_color or stream_type == StreamType.sphere_shape_radius:
            context.write_int_array(value[1])
        else:
            context.write_long_array(value[1])

    def deserialize(self, version, context):
        raise NotImplementedError


class CreateStreamResult(serializer_fields.TypeSerializer):
    def version(self):
        return 2

    def name(self):
        return "StreamCreationResult"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        err = context.read_byte()
        id = context.read_uint()
        if version > 0:
            data_type = StreamDataType(context.read_byte())
        else:
            data_type = StreamDataType.float
        if version >= 2:
            direction = StreamDirection(context.read_byte())
        else:
            direction = StreamDirection.writing
        return (err, id, data_type, direction)


class DestroyStream(serializer_fields.TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "StreamDestruction"

    def serialize(self, version, value, context):
        context.write_uint(value)

    def deserialize(self, version, context):
        raise NotImplementedError


class FeedStream(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__array = serializer_fields.ArrayField()
        self.__array.set_type(serializer_fields.StringField())

    def version(self):
        return 2

    def name(self):
        return "StreamFeed"

    def serialize(self, version, value, context):
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


class FeedStreamDone(serializer_fields.TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "StreamFeedDone"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return None


class InterruptStream(serializer_fields.TypeSerializer):
    def version(self):
        return 0

    def name(self):
        return "StreamInterrupt"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        err = context.read_byte()
        id = context.read_uint()
        return (err, id)
