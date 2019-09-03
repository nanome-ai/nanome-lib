from nanome._internal._util._serializers import _StringSerializer
from nanome._internal._util._serializers import _TypeSerializer


class _OpenURL(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "OpenURL"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string, value)

    def deserialize(self, version, context):
        raise NotImplementedError
