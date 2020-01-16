from nanome._internal._util._serializers import _TypeSerializer, _UnityPositionSerializer, _UnityRotationSerializer, _Vector3Serializer


class _GetMenuTransformResponse(_TypeSerializer):
    def __init__(self):
        self.pos = _UnityPositionSerializer()
        self.rot = _UnityRotationSerializer()
        self.vec3 = _Vector3Serializer()

    def version(self):
        return 0

    def name(self):
        return "GetMenuTransformResponse"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        menu_position = context.read_using_serializer(self.pos)
        menu_rotation = context.read_using_serializer(self.rot)
        menu_scale = context.read_using_serializer(self.vec3)

        result = (menu_position, menu_rotation, menu_scale)
        return result
