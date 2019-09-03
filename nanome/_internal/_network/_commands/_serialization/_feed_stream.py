from nanome._internal._util._serializers import _TypeSerializer
import nanome

class _FeedStream(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 1

    def name(self):
        return "StreamFeed"

    def serialize(self, version, value, context):
        context.write_uint(value[0])
        data_type = value[2]
        if version > 0:
            context.write_byte(data_type)
        if data_type == nanome.api.streams.Stream.DataType.byte:
            context.write_byte_array(value[1])
        else:
            context.write_float_array(value[1])

    def deserialize(self, version, context):
        raise NotImplementedError