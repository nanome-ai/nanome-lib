from nanome.util import IntEnum
from . import _UIBaseSerializer
from .. import _Image
from nanome._internal._util._serializers import _ColorSerializer, _ArraySerializer, _ByteSerializer, _StringSerializer, _TypeSerializer

class _ImageSerializer(_TypeSerializer):
    def __init__(self):
        self.data = _ArraySerializer()
        self.data.set_type(_ByteSerializer())
        self.color = _ColorSerializer()
        self.string = _StringSerializer()

    def version(self):
        return 1

    def name(self):
        return "Image"

    def serialize(self, version, value, context):
        if (version == 0 ):
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= value._content_id
        else:
            safe_id = value._content_id
        context.write_int(safe_id)
        context.write_using_serializer(self.string, value._file_path)
        context.write_using_serializer(self.color, value._color)
        context.write_uint(value._scaling_option)
        data = []
        if (value._file_path != ""):
            with open(value._file_path, "rb") as f:
                data = f.read()
        context.write_using_serializer(self.data, data)

    def deserialize(self, version, context):
        value = _Image._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask
        value._file_path = context.read_using_serializer(self.string)
        value._color = context.read_using_serializer(self.color)
        value._scaling_option = context.read_uint()
        context.read_using_serializer(self.data) #skipping data.
        return value

_UIBaseSerializer.register_type("Image", _UIBaseSerializer.ContentType.eimage, _ImageSerializer())
