from nanome.util import IntEnum
from .. import _TextInput
from nanome._internal._util._serializers import _StringSerializer
from . import _UIBaseSerializer

from nanome._internal._util._serializers import _TypeSerializer

class _TextInputSerializer(_TypeSerializer):
    def __init__(self):
        self.string = _StringSerializer()
    
    def version(self):
        return 0

    def name(self):
        return "TextInput"

    def serialize(self, version, value, context):
        context.write_int(value._content_id)
        context.write_int(value._max_length)
        context.write_using_serializer(self.string, value._placeholder_text)
        context.write_using_serializer(self.string, value._input_text)
        pass

    def deserialize(self, version, context):
        value = _TextInput._create()
        value._content_id = context.read_int()
        value._max_length = context.read_int()
        value._placeholder_text = context.read_using_serializer(self.string)
        value._input_text = context.read_using_serializer(self.string)

        return value

_UIBaseSerializer.register_type("TextInput", _UIBaseSerializer.ContentType.etextInput, _TextInputSerializer())