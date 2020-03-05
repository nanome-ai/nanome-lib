from nanome.util import IntEnum
from .. import _TextInput
from nanome._internal._util._serializers import _StringSerializer
from . import _UIBaseSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _TextInputSerializer(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()
    
    def version(self):
        return 2

    def name(self):
        return "TextInput"

    def serialize(self, version, value, context):
        if (version == 0 ):
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= value._content_id
        else:
            safe_id = value._content_id
        context.write_int(safe_id)
        context.write_int(value._max_length)
        context.write_using_serializer(self.string, value._placeholder_text)
        context.write_using_serializer(self.string, value._input_text)
        if version >= 2:
            context.write_bool(value._password)
            context.write_bool(value._number)

    def deserialize(self, version, context):
        value = _TextInput._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask
        value._max_length = context.read_int()
        value._placeholder_text = context.read_using_serializer(self.string)
        value._input_text = context.read_using_serializer(self.string)
        if version >= 2:
            value._password = context.read_bool()
            value._number = context.read_bool()
        return value

_UIBaseSerializer.register_type("TextInput", _UIBaseSerializer.ContentType.etextInput, _TextInputSerializer())