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
        return 1

    def name(self):
        return "List"

    def serialize(self, version, value, context):
        if (version == 0 ):
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= value._content_id
        else:
            safe_id = value._content_id
        context.write_int(safe_id)
        context.write_using_serializer(self._array, value._items)
        context.write_int(value._display_columns)
        context.write_int(value._display_rows)
        context.write_int(value._total_columns)
        context.write_bool(value._unusable)

    def deserialize(self, version, context):
        value = _UIList._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask
        value._items = context.read_using_serializer(self._array)
        value._display_columns = context.read_int()
        value._display_rows = context.read_int()
        value._total_columns = context.read_int()
        value._unusable = context.read_bool()
        return value

_UIBaseSerializer.register_type("UIList", _UIBaseSerializer.ContentType.elist, _UIListSerializer())