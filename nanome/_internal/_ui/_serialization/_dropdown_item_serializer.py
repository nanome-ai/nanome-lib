from . import _UIBaseSerializer
from .. import _DropdownItem
from nanome._internal._util._serializers import _StringSerializer, _TypeSerializer

class _DropdownItemSerializer(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "DropdownItem"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string, value._name)
        context.write_bool(value._selected)
        context.write_bool(value._close_on_selected)
        context.write_byte(1)

    def deserialize(self, version, context):
        value = _DropdownItem._create()
        value._name = context.read_using_serializer(self.string)
        value._selected = context.read_bool()
        value._close_on_selected = context.read_bool()
        context.read_byte() #eat the type for now, since it isn't supported quite yet
        return value