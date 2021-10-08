from nanome._internal._util._serializers import _TypeSerializer
from nanome._internal._shapes._mesh import _Mesh


class _MeshSerializer(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "MeshShape"

    def serialize(self, version, value, context):
        context.write_float_array(value.vertices)
        context.write_float_array(value.normals)
        context.write_float_array(value.colors)
        context.write_int_array(value.triangles)
        context.write_float_array(value.uv)

    def deserialize(self, version, context):
        result = _Mesh._create()
        result.vertices = context.read_float_array()
        result.normals = context.read_float_array()
        result.colors = context.read_float_array()
        result.triangles = context.read_int_array()
        result.uv = context.read_float_array()
        return result
