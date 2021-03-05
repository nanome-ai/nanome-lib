from nanome._internal._network._serialization import _ContextDeserialization, _ContextSerialization
from nanome._internal._util._serializers import _StringSerializer
from nanome._internal._util._serializers import _TypeSerializer

class _SendNotification(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "SendNotification"

    def serialize(self, version, value, context):
        context.write_uint(value[0])
        context.write_using_serializer(self.string, value[1])

    def deserialize(self, version, context):
        raise NotImplementedError