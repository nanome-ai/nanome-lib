from nanome._internal._util._serializers import _ArraySerializer, _LongSerializer
from nanome._internal._util._serializers import _TypeSerializer

class _CreateStream(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 2

    def name(self):
        return "StreamCreation"

    def serialize(self, version, value, context):
        if version > 0:
            context.write_byte(value[0])
        if version >= 2:
            context.write_byte(value[2])
        context.write_long_array(value[1])

    def deserialize(self, version, context):
        raise NotImplementedError