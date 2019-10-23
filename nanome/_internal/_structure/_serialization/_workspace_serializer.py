from nanome._internal._util._serializers import _ArraySerializer, _UnityPositionSerializer, _UnityRotationSerializer, _Vector3Serializer
from . import _ComplexSerializer
from .. import _Workspace

from nanome._internal._util._serializers import _TypeSerializer

class _WorkspaceSerializer(_TypeSerializer):
    def __init__(self):
        self.array = _ArraySerializer()
        self.array.set_type(_ComplexSerializer())
        self.vec = _Vector3Serializer()
        self.pos = _UnityPositionSerializer()
        self.rot = _UnityRotationSerializer()

    def version(self):
        return 0

    def name(self):
        return "Workspace"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.array, value._complexes)

        context.write_using_serializer(self.pos, value._position)
        context.write_using_serializer(self.rot, value._rotation)
        context.write_using_serializer(self.vec, value._scale)

    def deserialize(self, version, context):
        workspace = _Workspace._create()
        workspace._complexes = context.read_using_serializer(self.array)
        workspace._position = context.read_using_serializer(self.pos)
        workspace._rotation = context.read_using_serializer(self.rot)
        workspace._scale = context.read_using_serializer(self.vec)

        return workspace