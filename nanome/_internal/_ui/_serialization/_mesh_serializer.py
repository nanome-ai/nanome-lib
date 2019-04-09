from . import _UIBaseSerializer
from .. import _Mesh
from nanome.util import IntEnum
from nanome._internal._util._serializers import _ColorSerializer, _TypeSerializer

class _MeshSerializer(_TypeSerializer):
    def __init__(self):
        self.color = _ColorSerializer()

    def version(self):
        return 0

    def name(self):
        return "Mesh"

    def serialize(self, version, value, context):
        context.write_int(value._content_id)
        context.write_using_serializer(self.color, value._mesh_color)

    def deserialize(self, version, context):
        value = _Mesh._create()
        value._content_id = context.read_int()
        value._mesh_color = context.read_using_serializer(self.color)
        return value

_UIBaseSerializer.register_type("Mesh", _UIBaseSerializer.ContentType.emesh, _MeshSerializer())
