from nanome._internal._ui._serialization import _UIBaseSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _UpdateContent(_TypeSerializer):
    def __init__(self):
        self.content = _UIBaseSerializer()

    def version(self):
        return 0

    def name(self):
        return "SendUIContent"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.content, value)

    def deserialize(self, version, context):
        return None