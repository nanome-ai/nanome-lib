from nanome._internal._util._serializers import _StringSerializer
from nanome._internal._util._serializers import _TypeSerializer


class _OpenURL(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()

    def version(self):
        return 1

    def name(self):
        return "OpenURL"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string, value[0])  # URL
        if version >= 1:
            context.write_bool(value[1])  # Desktop Browser

    def deserialize(self, version, context):
        raise NotImplementedError
