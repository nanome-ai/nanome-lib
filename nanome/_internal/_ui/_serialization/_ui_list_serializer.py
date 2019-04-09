from nanome._internal._util._serializers import _ArraySerializer
from nanome._internal._ui._serialization import _LayoutNodeSerializerDeep
from . import _UIBaseSerializer
from .. import _UIList

from nanome._internal._util._serializers import _TypeSerializer

class _UIListSerializer(_TypeSerializer):
    def __init__(self):
        self._array = _ArraySerializer()
        self._array.set_type(_LayoutNodeSerializerDeep())

    def version(self):
        return 0

    def name(self):
        return "List"

    def serialize(self, version, value, context):
        context.write_int(value._content_id)
        context.write_using_serializer(self._array, value._items)
        context.write_int(value._display_columns)
        context.write_int(value._display_rows)
        context.write_int(value._total_columns)
        context.write_bool(value._unusable)

    def deserialize(self, version, context):
        result = _UIList._create()
        result._content_id = context.read_int()
        result._items = context.read_using_serializer(self._array)
        result._display_columns = context.read_int()
        result._display_rows = context.read_int()
        result._total_columns = context.read_int()
        result._unusable = context.read_bool()
        return result

_UIBaseSerializer.register_type("UIList", _UIBaseSerializer.ContentType.elist, _UIListSerializer())