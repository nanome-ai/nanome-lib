from nanome._internal._util._serializers import _ArraySerializer, _QuaternionSerializer, _Vector3Serializer
from . import _ComplexSerializer
from .. import _Workspace

from nanome._internal._util._serializers import _TypeSerializer

class _WorkspaceSerializer(_TypeSerializer):
    def __init__(self):
        self.array = _ArraySerializer()
        self.array.set_type(_ComplexSerializer())
        self.vector = _Vector3Serializer()
        self.quaternion = _QuaternionSerializer()

    def version(self):
        return 0

    def name(self):
        return "Workspace"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.array, value._complexes)

        context.write_using_serializer(self.vector, value.transform._position)
        context.write_using_serializer(self.quaternion, value.transform._rotation)
        context.write_using_serializer(self.vector, value.transform._scale)

    def deserialize(self, version, context):
        workspace = _Workspace._create()
        workspace._complexes = context.read_using_serializer(self.array)
        workspace._transform._position = context.read_using_serializer(self.vector)
        workspace._transform._rotation = context.read_using_serializer(self.quaternion)
        workspace._transform._scale = context.read_using_serializer(self.vector)

        return workspace