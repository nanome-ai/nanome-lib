from nanome.util.enum import safe_cast
from nanome._internal._util._serializers import _TypeSerializer, _UnityPositionSerializer
from nanome._internal._shapes import _Anchor
from nanome.util.enums import ShapeType

class _AnchorSerializer(_TypeSerializer):
    def __init__(self):
        self._offset = _UnityPositionSerializer()

    def version(self):
        return 0

    def name(self):
        return "SetShape"

    def serialize(self, version, value, context):
        context.write_int(value._target)
        context.write_using_serializer(self._offset, value._offset)
        context.write_byte(int(value._anchor_type))

    def deserialize(self, version, context):
        result = _Anchor._create()
        result._target = context.read_int()
        result._offset = context.read_using_serializer(self._offset)
        result._anchor_type = ShapeType.safe_cast(context.read_byte())
        return result