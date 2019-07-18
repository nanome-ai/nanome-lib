from . import _UIBaseSerializer
from .. import _Mesh
from nanome.util import IntEnum
from nanome._internal._util._serializers import _ColorSerializer, _TypeSerializer

class _MeshSerializer(_TypeSerializer):
    def __init__(self):
        self.color = _ColorSerializer()

    def version(self):
        return 1

    def name(self):
        return "Mesh"

    def serialize(self, version, value, context):
        if (version == 0 ):
            safe_id = (context._plugin_id << 24) & 0x7FFFFFFF
            safe_id |= value._content_id
        else:
            safe_id = value._content_id
        context.write_int(safe_id)
        context.write_using_serializer(self.color, value._mesh_color)

    def deserialize(self, version, context):
        value = _Mesh._create()
        value._content_id = context.read_int()
        if (version == 0):
            id_mask = 0x00FFFFFF
            value._content_id &= id_mask
        value._mesh_color = context.read_using_serializer(self.color)
        return value

_UIBaseSerializer.register_type("Mesh", _UIBaseSerializer.ContentType.emesh, _MeshSerializer())
