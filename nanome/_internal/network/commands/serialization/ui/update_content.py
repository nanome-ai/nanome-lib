from nanome._internal.ui._serialization import _UIBaseSerializer
from nanome._internal.util.serializers import _ArraySerializer
from nanome._internal.util.serializers import TypeSerializer


class _UpdateContent(TypeSerializer):
    def __init__(self):
        self._array = _ArraySerializer()
        self._content = _UIBaseSerializer()
        self._array.set_type(self._content)

    def version(self):
        return 1

    def name(self):
        return "SendUIContent"

    def serialize(self, version, value, context):
        if version == 0:
            context.write_using_serializer(self._content, value[0])
        else:
            context.write_using_serializer(self._array, value)

    def deserialize(self, version, context):
        return None
