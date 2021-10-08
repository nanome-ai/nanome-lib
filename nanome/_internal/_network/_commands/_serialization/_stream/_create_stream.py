from nanome._internal._util._serializers import _ArraySerializer, _LongSerializer
from nanome._internal._util._serializers import _TypeSerializer
from nanome.util.enums import StreamType as SType


class _CreateStream(_TypeSerializer):
    def __init__(self):
        pass

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

        if stream_type == SType.shape_position or stream_type == SType.shape_color or stream_type == SType.sphere_shape_radius:
            context.write_int_array(value[1])
        else:
            context.write_long_array(value[1])

    def deserialize(self, version, context):
        raise NotImplementedError
