from nanome._internal.util.type_serializers import ArraySerializer, UnityPositionSerializer, UnityRotationSerializer, Vector3Serializer
from . import _ComplexSerializer
from .. import _Workspace

from nanome._internal.util.type_serializers import TypeSerializer


class _WorkspaceSerializer(TypeSerializer):
    def __init__(self):
        self.array = ArraySerializer()
        self.array.set_type(_ComplexSerializer())
        self.vec = Vector3Serializer()
        self.pos = UnityPositionSerializer()
        self.rot = UnityRotationSerializer()

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
