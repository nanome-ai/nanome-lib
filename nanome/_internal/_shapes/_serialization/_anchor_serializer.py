from nanome._internal._util._serializers import _TypeSerializer, _UnityPositionSerializer
from nanome._internal._shapes import _Anchor
from nanome.util.enums import ShapeType


class _AnchorSerializer(_TypeSerializer):
    def __init__(self):
        self._offset = _UnityPositionSerializer()

    def version(self):
        return 0

    def name(self):
        return "ShapeAnchor"

    def serialize(self, version, value, context):
        context.write_long(value._target)
        context.write_byte(int(value._anchor_type))
        context.write_using_serializer(self._offset, value._local_offset)
        context.write_using_serializer(self._offset, value._global_offset)
        context.write_using_serializer(self._offset, value._viewer_offset)

    def deserialize(self, version, context):
        result = _Anchor._create()
        result._target = context.read_long()
        result._anchor_type = ShapeType.safe_cast(context.read_byte())
        result._local_offset = context.read_using_serializer(self._offset)
        result._global_offset = context.read_using_serializer(self._offset)
        result._viewer_offset = context.read_using_serializer(self._offset)
        return result
