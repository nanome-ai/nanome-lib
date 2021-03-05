from . import _UIBaseSerializer
from . import _DropdownItemSerializer
from .. import _Dropdown
from nanome._internal._util._serializers import _StringSerializer, _ArraySerializer, _TypeSerializer

class _DropdownSerializer(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()
        self.items = _ArraySerializer()
        self.items.set_type(_DropdownItemSerializer())

    def version(self):
        return 0

    def name(self):
        return "Dropdown"

    def serialize(self, version, value, context):
        context.write_int(value._content_id)
        context.write_bool(value._use_permanent_title)
        context.write_using_serializer(self.string, value._permanent_title)
        context.write_int(value._max_displayed_items)
        context.write_using_serializer(self.items, value._items)

    def deserialize(self, version, context):
        value = _Dropdown._create()
        value._content_id = context.read_int()
        value._use_permanent_title = context.read_bool()
        value._permanent_title = context.read_using_serializer(self.string)
        value._max_displayed_items = context.read_int()
        value._items = context.read_using_serializer(self.items)
        return value

_UIBaseSerializer.register_type("Dropdown", _UIBaseSerializer.ContentType.edropdown, _DropdownSerializer())
