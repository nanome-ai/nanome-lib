from nanome._internal._util._serializers import _TypeSerializer
from nanome.util.enums import StreamDataType, StreamDirection

class _CreateStreamResult(_TypeSerializer):
    def __init__(self):
        pass

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
